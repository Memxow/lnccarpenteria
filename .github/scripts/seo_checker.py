import os
import glob
import time
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY non trovata nei Secret di GitHub!")

client = genai.Client(api_key=api_key)
active_model = 'gemini-3.8-flash'

# Selezioniamo SOLO le pagine strategiche per la SEO per evitare di esaurire la quota giornaliera
target_pages = [
    "index.html",
    "services.html",
    "about.html",
    "contacts.html",
    "en/index.html",
    "en/services.html",
    "en/about.html",
    "en/contacts.html"
]

report = []

print(f"🚀 Avvio analisi SEO strategica con il modello {active_model}...")

for file_path in target_pages:
    if not os.path.exists(file_path):
        continue

    print(f"Analisi in corso per: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = f"""
    Sei un esperto SEO specializzato nel settore della carpenteria metallica e lavorazioni industriali.
    Analizza il codice HTML del file '{file_path}':

    {content[:3500]}

    Fornisci un'analisi strutturata in italiano contenente:
    1. **Meta Title Consigliato**: (max 65 caratteri, ottimizzato per keyword di settore e geolocalizzazione).
    2. **Meta Description Consigliata**: (max 160 caratteri, persuasiva e ricca di keyword).
    3. **Keyword Strategiche Rilevate/Consigliate**: 3-5 parole chiave pertinenti per questa pagina.
    4. **3 Suggerimenti Pratici di Contenuto**: Suggerimenti specifici per migliorare il posizionamento Google del testo.
    """

    try:
        response = client.models.generate_content(
            model=active_model,
            contents=prompt
        )
        report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n{response.text}\n\n---\n")
        # Breve pausa per rispettare i rate limit della API gratuita
        time.sleep(4)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n*⚠️ Limite quota giornaliera raggiunto (Free Tier). Le analisi successive riprenderanno domani.* \n\n---\n")
            print("Quota giornaliera esaurita, interrotto l'invio di nuove richieste.")
            break
        else:
            report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n*Errore durante l'analisi: {e}*\n\n---\n")

with open("SEO_RECOMMENDATIONS.md", "w", encoding="utf-8") as f:
    f.write(f"# 📈 Report SEO con Suggerimenti IA\n\n*Modello utilizzato: {active_model}*\n\n" + "".join(report))

print("Analisi SEO IA completata con successo!")