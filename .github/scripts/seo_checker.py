import os
import glob
from google import genai

# Recupera la chiave API dai Secret
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY non trovata nei Secret di GitHub!")

# Inizializza il client Gemini aggiornato
client = genai.Client(api_key=api_key)

html_files = glob.glob("**/*.html", recursive=True)
report = []

for file_path in html_files:
    # Ignora componenti e file non utili alla SEO di pagina
    if any(x in file_path for x in ["404.html", "google", "header.html", "footer.html"]):
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
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n{response.text}\n\n---\n")
    except Exception as e:
        report.append(f"Errore durante l'analisi di {file_path}: {e}\n\n---\n")

with open("SEO_RECOMMENDATIONS.md", "w", encoding="utf-8") as f:
    f.write("# 📈 Report SEO con Suggerimenti IA (Gemini)\n\n" + "".join(report))

print("Analisi SEO IA completata con successo!")