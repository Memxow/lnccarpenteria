import os
import glob
from bs4 import BeautifulSoup

html_files = glob.glob('**/*.html', recursive=True)
report = []

for file_path in html_files:
    if "404.html" in file_path:
        continue

    with open(file_path, "r" , encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    issues = []

    #Controlla il Titolo
    title = soup.find('title')
    if not title or not title.string.strip():
        issues.append("Manca il tag `<title>` o è vuoto.")
    elif len(title.string) > 60:
        issues.append(f"Il `<title>` è troppo ({len(title.string)} caratteri). Consigliato: max 60.")

    #Controlla la Meta Description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if not meta_desc or not meta_desc.get('content', '').strip():
        issues.append("Manca la `<meta name='description'>`.")
    elif len(meta_desc.get('content', '')) > 160:
        issues.append(f"La `meta description` è troppo lunga. Consigliato: max 155-160 caratteri.")

    #Controlla h1
    h1s = soup.find_all('h1')
    if len(h1s) == 0:
        issues.append("Manca il tag `<h1>` nella pagina.")
    elif len(h1s) > 1:
        issues.append(f"Ci sono {len(h1s)} tag `<h1>`. E' consigliato averne uno solo per pagina.")

    #Controlla le immagini senza alt
    imgs = soup.find_all('img')
    missing_alt = [img.get('src', 'immagine sconosciuta') for img in imgs if not img.get('alt')]
    if missing_alt:
        issues.append(f"Immagini senza attributo `alt`: {len(missing_alt)} trovate.")

    #Aggiungi al report 
    report.append(f"## Analisi per `{file_path}`\n")
    if issues:
        for issue in issues:
            report.append(f"- {issue}\n")

    else: 
        report.append("- Nessun problema SEO critico rilevato!\n")
    report.append("\n--\n")

with open("SEO_RECOMMENDATIONS.md", "w", encoding="utf-8") as f:
    f.write("# Report SEO Automatico (Controllo Strutturale)\n\n" + "".join(report))

print("Controllo SEO completato con successo!")