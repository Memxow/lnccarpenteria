import os
import glob
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY non trovata nei Secret di GitHub!")

client = genai.Client(api_key=api_key)

candidate_models = []

print("🔍 Interrogazione dei server di Google per estrarre TUTTI i modelli disponibili...")
try:
    all_models = list(client.models.list())
    for m in all_models:
        model_name = m.name.replace('models/', '')
        methods = getattr(m, 'supported_generation_methods', [])
        if 'generateContent' in methods:
            if model_name not in candidate_models:
                candidate_models.append(model_name)
    print(f"Modelli trovati dall'API: {candidate_models}")
except Exception as e:
    print(f"Impossibile elencare i modelli via API: {e}")

# Aggiungiamo comunque una lista massiccia ed esaustiva di TUTTI i modelli Gemini possibili
exhaustive_fallback = [
    'gemini-2.5-flash',
    'gemini-2.0-flash',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-pro',
    'gemini-1.0-pro',
    'gemini-pro-vision',
    'gemini-flash'
]

for fb in exhaustive_fallback:
    if fb not in candidate_models:
        candidate_models.append(fb)

print(f"📋 Lista totale di modelli da testare uno a uno ({len(candidate_models)} modelli): {candidate_models}")

active_model = None

# PROVA TUTTI I MODELLI FINCHÈ UNO FUNZIONA
for model_candidate in candidate_models:
    try:
        print(f"🧪 Test in corso con il modello: {model_candidate}...")
        test_resp = client.models.generate_content(
            model=model_candidate,
            contents="Test di connessione SEO"
        )
        active_model = model_candidate
        print(f"🎉 SUCCESSO! Trovato il primo modello funzionante: {active_model}")
        break
    except Exception as e:
        print(f"❌ {model_candidate} scartato: {e}")

if not active_model:
    raise RuntimeError("❌ ERRORE CRITICO: Ho provato TUTTI i modelli esistenti ma nessuno ha risposto positivamente con questa chiave API.")

print(f"🚀 Procedo con l'analisi HTML usando il modello confermato: {active_model}")

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
        response = client.models.generate_content(
            model=active_model,
            contents=prompt
        )
        report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n{response.text}\n\n---\n")
    except Exception as e:
        report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n*Errore durante l'analisi: {e}*\n\n---\n")

with open("SEO_RECOMMENDATIONS.md", "w", encoding="utf-8") as f:
    f.write(f"# 📈 Report SEO con Suggerimenti IA\n\n*Modello testato e funzionante: {active_model}*\n\n" + "".join(report))

print("Analisi SEO IA completata con successo!")