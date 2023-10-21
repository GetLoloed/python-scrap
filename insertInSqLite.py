import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


# Fonction pour extraire l'information de l'épisode
def extract_episode_info(serie_episode):
    pattern = r'saison (\d+) episode (\d+)'
    match = re.search(pattern, serie_episode, re.IGNORECASE)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


# Fonction pour scraper les données
def scrape_spin_off():
    URL = "https://www.spin-off.fr/calendrier_des_series.html?date=2023-10"
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    all_series_data = []

    for cell in soup.select(".floatleftmobile.td_jour"):
        date_div = cell.select_one(".div_jour")
        if date_div:
            date = re.search(r'(\d{2}-\d{2}-\d{4})', date_div.select_one("a")["href"]).group(1)

            for serie in cell.select(".calendrier_episodes"):
                links = serie.select("a")
                serie_name = links[0].text
                serie_episode = links[1]["title"]
                h_ref = links[1]["href"]
                n_saison, n_episode = extract_episode_info(serie_episode)

                # Ajustement pour récupérer correctement le pays et la chaîne
                icons = serie.find_all_previous("img", {"alt": True}, limit=2)
                if len(icons) == 2:
                    channel = icons[0]["alt"]
                    country = icons[1]["alt"]
                else:
                    channel, country = None, None

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


# Récupération des données
all_series_data = scrape_spin_off()

# Créer une connexion et un curseur
path = 'data/databases'
if not os.path.exists(path):
    os.makedirs(path)

conn = sqlite3.connect(os.path.join(path, 'database.db'))
cursor = conn.cursor()

# Créer la table episode
cursor.execute('''
CREATE TABLE IF NOT EXISTS episode (
    id INTEGER PRIMARY KEY,
    serie_name TEXT NOT NULL,
    n_episode INTEGER,
    n_saison INTEGER,
    channel TEXT,
    country TEXT,
    h_ref TEXT,
    date TEXT
)
''')

# Insérer les données dans la table
for series in all_series_data:
    cursor.execute('''
    INSERT INTO episode (serie_name, n_episode, n_saison, channel, country, h_ref, date) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (series["serie_name"], series["n_episode"], series["n_saison"], series["channel"], series["country"],
          series["h_ref"], series["date"]))

# Commit the transaction
conn.commit()

# Afficher les données avec pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Lire la table 'episode' dans un DataFrame
df = pd.read_sql_query('SELECT * FROM episode', conn)

# Afficher les données
print(df.head())  # Afficher les 5 premières lignes avec toutes les colonnes

# Fermer la connexion
conn.close()
