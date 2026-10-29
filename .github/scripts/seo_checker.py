import os
import glob
import google.generativeai as genai

#Configurazione API con la chiave salvata nei Secret di Github
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY non trovata nei Secreti di GitHub")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

html_files = glob.glob("**/*.html", recursive = True)
report = []

for file_path in html_files:
    #Ignora file si sistema, componenti non usati e pagine di verifica
    if "404.html" in file_path or "google" in file_path or "header.html" in file_path or "footer.html" in file_path:
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = f"""
    Sei un esperto SEO specializzato nel settore della carpenteria metallica e lavorazioni industriali.
    Analizza il codice HTML del file '{file_path}':

    {content[:3500]}

    Fornisci un'analisi strutturata in italiano contenente:
    1. **Meta Title Consigliato**: (max 60 caratteri, ottimizzato per keyword di settore).
    2. **Meta Description Consigliata**: (max 155 caratteri, persuasiva e ricca di keyword).
    3. **Keyword Strategiche Rilevate/Consigliate**: 3-5 parole chiave pertinenti per questa pagina.
    4. **3 Suggerimenti Pratici di Contenuto**: Suggerimenti specifici per migliorare il posizionamento Google del testo.
    """

    try:
        response = model.generate_content(prompt)
        report.append(f'## Analisi IA per `{file_path}`\n\n{response.text}\n\n--\n')
    except Exception as e:
        report.append(f"Errore durante l'analisi di {file_path}: {e}\n\n--\n")

with open("SEO_RECOMMENDATIONS.md", "w", encoding="utf-8") as f:
    f.write("# Analisi SEO con suggerimenti IA (Gemini)\n\n" + "".join(report))

print("Analisi SEO AI completata con successo!")
