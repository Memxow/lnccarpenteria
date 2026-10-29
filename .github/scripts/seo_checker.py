import os
import glob
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY non trovata nei Secret di GitHub!")

client = genai.Client(api_key=api_key)

# Inseriamo subito in cima il modello richiesto dai server di Google
candidate_models = ['gemini-3.8-flash']

try:
    all_models = list(client.models.list())
    for m in all_models:
        model_name = m.name.replace('models/', '')
        methods = getattr(m, 'supported_generation_methods', [])
        if 'generateContent' in methods:
            if model_name not in candidate_models:
                candidate_models.append(model_name)
except Exception as e:
    print(f"Impossibile elencare i modelli via API: {e}")

exhaustive_fallback = [
    'gemini-3.8-flash',
    'gemini-2.5-flash',
    'gemini-2.0-flash',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-pro',
    'gemini-flash'
]

for fb in exhaustive_fallback:
    if fb not in candidate_models:
        candidate_models.append(fb)

print(f"📋 Lista totale di modelli da testare: {candidate_models}")

active_model = None

for model_candidate in candidate_models:
    try:
        print(f"🧪 Test con il modello: {model_candidate}...")
        test_resp = client.models.generate_content(
            model=model_candidate,
            contents="Test"
        )
        active_model = model_candidate
        print(f"✅ Trovato modello funzionante: {active_model}")
        break
    except Exception as e:
        print(f"❌ {model_candidate} scartato: {e}")

if not active_model:
    raise RuntimeError("❌ Nessun modello compatibile trovato con questa chiave API.")

print(f"🚀 Procedo con l'analisi HTML usando il modello: {active_model}")

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
    1. **Meta Title Consigliato**: (max 65 caratteri, ottimizzato per keyword di settore).
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
    except Exception as e:
        report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n*Errore durante l'analisi: {e}*\n\n---\n")

with open("SEO_RECOMMENDATIONS.md", "w", encoding="utf-8") as f:
    f.write(f"# 📈 Report SEO con Suggerimenti IA\n\n*Modello utilizzato: {active_model}*\n\n" + "".join(report))

print("Analisi SEO IA completata con successo!")