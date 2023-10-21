import requests
from bs4 import BeautifulSoup
import re


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

# Parcours des éléments de la page
for cell in soup.select(".floatleftmobile.td_jour"):
    date_div = cell.select_one(".div_jour")
    if date_div:
        # Extraction de la date au format YYYYMMDD
        date = re.search(r'(\d{2}-\d{2}-\d{4})', date_div.select_one("a")["href"]).group(1)
        date = date.replace("-", "")

        # Initialisation de country et channel avant d'extraire les séries
        country = ""
        channel = ""

        for item in cell.contents:
            if isinstance(item, type(soup.new_tag("test"))):  # Vérification si l'élément est une balise HTML
                if item.name == "img":
                    if "/images/pays/" in item["src"]:
                        country = item["alt"]
                    elif "/images/chaines/" in item["src"]:
                        channel = item["alt"]

                elif item.has_attr("class") and "calendrier_episodes" in item["class"]:
                    # Extraction des informations nécessaires
                    links = item.select("a")
                    serie_name = links[0].text
                    serie_episode = links[1]["title"]
                    h_ref = links[1]["href"]
                    n_saison, n_episode = extract_episode_info(serie_episode)

                    # Ajout des données à la liste
                    series_data = {
                        "serie_name": serie_name,
                        "serie_episode": serie_episode,
                        "channel": channel,
                        "country": country,
                        "h_ref": h_ref,
                        "date": date,
                        "n_saison": n_saison,
                        "n_episode": n_episode,
                    }
                    all_series_data.append(series_data)

# Affichage des données extraites
print(all_series_data)
