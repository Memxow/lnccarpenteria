import os
import glob
import signal
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY non trovata nei Secret di GitHub!")

genai.configure(api_key=api_key)

model_name = 'gemini-1.5-flash'
print(f"Utilizzo del modello: {model_name}")
model = genai.GenerativeModel(model_name)

# Gestione del timeout per evitare blocchi infiniti su GitHub Actions (Linux)
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Timeout della richiesta API")

signal.signal(signal.SIGALRM, timeout_handler)

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
        # Imposta un limite massimo di 25 secondi per ogni file
        signal.alarm(25)
        response = model.generate_content(prompt)
        signal.alarm(0)  # Disattiva l'allarme se ha risposto in tempo
        
        report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n{response.text}\n\n---\n")
    except TimeoutException:
        signal.alarm(0)
        report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n*⚠️ Saltato per timeout (la risposta ha impiegato troppo tempo).* \n\n---\n")
    except Exception as e:
        signal.alarm(0)
        report.append(f"## 🤖 Analisi IA per `{file_path}`\n\n*Errore durante l'analisi: {e}*\n\n---\n")

with open("SEO_RECOMMENDATIONS.md", "w", encoding="utf-8") as f:
    f.write(f"# 📈 Report SEO con Suggerimenti IA\n\n*Modello utilizzato: {model_name}*\n\n" + "".join(report))

print("Analisi SEO IA completata con successo!")