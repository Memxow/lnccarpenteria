import os
import glob
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY non trovata nei Secret di GitHub!")

genai.configure(api_key=api_key)

# Chiede direttamente a Google quali modelli sono supportati dalla tua chiave
selected_model_name = 'gemini-3.8-flash'  # Valore di sicurezza predefinito
try:
    available_models = [
        m.name for m in genai.list_models() 
        if 'generateContent' in m.supported_generation_methods
    ]
    print(f"Modelli disponibili trovati: {available_models}")
    
    # Cerca prima un modello flash, altrimenti prende il primo disponibile
    for m in available_models:
        if 'flash' in m:
            selected_model_name = m
            break
        elif available_models:
            selected_model_name = available_models[0]
except Exception as e:
    print(f"Impossibile elencare i modelli, uso il default: {e}")

print(f"-> Modello selezionato automaticamente: {selected_model_name}")
model = genai.GenerativeModel(selected_model_name)

html_files = glob.glob("**/*.html", recursive=True)
report = []

for file_path in html_files:
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
        response = model.generate_content(prompt)
        report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n{response.text}\n\n---\n")
    except Exception as e:
        report.append(f"Errore durante l'analisi di {file_path}: {e}\n\n---\n")

with open("SEO_RECOMMENDATIONS.md", "w", encoding="utf-8") as f:
    f.write(f"# 📈 Report SEO con Suggerimenti IA\n\n*Modello utilizzato: {selected_model_name}*\n\n" + "".join(report))

print("Analisi SEO IA completata con successo!")