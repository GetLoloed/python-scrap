import os
import requests
from bs4 import BeautifulSoup
import re
import psycopg2


# Fonction pour extraire l'information de l'épisode à partir de son titre
def extract_episode_info(serie_episode):
    pattern = r'saison (\d+) episode (\d+)'
    match = re.search(pattern, serie_episode, re.IGNORECASE)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


# Fonction pour scraper les données des séries du site spin-off pour un mois donné
def scrape_spin_off():
    # URL du calendrier des séries pour le mois d'octobre 2023
    URL = "https://www.spin-off.fr/calendrier_des_series.html?date=2023-10"
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    all_series_data = []

    # Parcourir chaque cellule du calendrier
    for cell in soup.select(".floatleftmobile.td_jour"):
        date_div = cell.select_one(".div_jour")
        if date_div:
            # Extraire la date de diffusion de l'épisode
            date = re.search(r'(\d{2}-\d{2}-\d{4})', date_div.select_one("a")["href"]).group(1)

            # Extraire les informations de chaque série diffusée ce jour
            for serie in cell.select(".calendrier_episodes"):
                links = serie.select("a")
                serie_name = links[0].text
                serie_episode = links[1]["title"]
                h_ref = links[1]["href"]
                n_saison, n_episode = extract_episode_info(serie_episode)

                # Récupération du pays et de la chaîne de diffusion
                icons = serie.find_all_previous("img", {"alt": True}, limit=2)
                if len(icons) == 2:
                    channel = icons[0]["alt"]
                    country = icons[1]["alt"]
                else:
                    channel, country = None, None

                # Compilation des données dans un dictionnaire
                series_data = {
                    "serie_name": serie_name,
                    "n_saison": n_saison,
                    "n_episode": n_episode,
                    "channel": channel,
                    "country": country,
                    "h_ref": h_ref,
                    "date": date
                }
                all_series_data.append(series_data)

    return all_series_data


# Récupération des données des séries
all_series_data = scrape_spin_off()

# Connexion à la base de données PostgreSQL hébergée sur Scalingo
DATABASE_URL = "postgres://[...]"  # J'ai abrégé l'URL pour la lisibilité
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Création de la table 'episode' si elle n'existe pas déjà
create_table_sql = """
CREATE TABLE IF NOT EXISTS episode (
    id SERIAL PRIMARY KEY,
    serie_name TEXT NOT NULL,
    n_episode INTEGER,
    n_saison INTEGER,
    channel TEXT,
    country TEXT,
    h_ref TEXT,
    date TEXT
);
"""
cursor.execute(create_table_sql)
print("Table 'episode' créée avec succès.")

# Insertion des données des séries dans la table 'episode'
for series_data in all_series_data:
    insert_sql = """
    INSERT INTO episode (serie_name, n_episode, n_saison, channel, country, h_ref, date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(insert_sql, (
            series_data["serie_name"],
            series_data["n_episode"],
            series_data["n_saison"],
            series_data["channel"],
            series_data["country"],
            series_data["h_ref"],
            series_data["date"]
        ))
        print(f"Données pour {series_data['serie_name']} insérées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données pour {series_data['serie_name']}: {str(e)}")

# Validation des modifications et fermeture de la connexion à la base de données
conn.commit()
conn.close()
