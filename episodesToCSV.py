import requests
from bs4 import BeautifulSoup
import re
import os
import csv

# Fonction pour extraire l'information de l'épisode
def extract_episode_info(serie_episode):
    pattern = r'saison (\d+) episode (\d+)'
    match = re.search(pattern, serie_episode, re.IGNORECASE)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

# URL de la page à scraper
URL = "https://www.spin-off.fr/calendrier_des_series.html?date=2023-10"
response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
all_series_data = []

for cell in soup.select(".floatleftmobile.td_jour"):
    date_div = cell.select_one(".div_jour")
    if date_div:
        # Extraction de la date au format YYYYMMDD
        date = re.search(r'(\d{2}-\d{2}-\d{4})', date_div.select_one("a")["href"]).group(1)
        date = date.replace("-", "")

        # Récupération des images des pays et des chaînes
        country_imgs = cell.select("img[src^='/images/pays/']")
        channel_imgs = cell.select("img[src^='/images/chaines/']")

        for serie in cell.select(".calendrier_episodes"):
            links = serie.select("a")
            serie_name = links[0].text.strip()
            serie_episode = links[1]["title"]
            h_ref = links[1]["href"]
            n_saison, n_episode = extract_episode_info(serie_episode)

            country = country_imgs[0]["alt"] if country_imgs else ""
            channel = channel_imgs[0]["alt"] if channel_imgs else ""

            series_data = {
                "serie_name": serie_name,
                "n_episode": n_episode,
                "n_saison": n_saison,
                "channel": channel,
                "country": country,
                "h_ref": h_ref,
                "date": date
            }
            all_series_data.append(series_data)

# Vérifier si le chemin existe, sinon le créer
path = 'data/files'
if not os.path.exists(path):
    os.makedirs(path)

# Nom de fichier
filename = os.path.join(path, 'episodes.csv')

# Écriture dans le fichier CSV
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['serie_name', 'n_episode', 'n_saison', 'channel', 'country', 'h_ref', 'date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

    for serie_data in all_series_data:
        writer.writerow(serie_data)