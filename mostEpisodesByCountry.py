import os
import sqlite3

# Établir la connexion avec la base de données SQLite
path = 'data/databases'
conn = sqlite3.connect(os.path.join(path, 'database.db'))
cursor = conn.cursor()

cursor.execute("""
SELECT country, COUNT(country) as count
FROM episode
GROUP BY country
ORDER BY count DESC
""")
country_counts = cursor.fetchall()
conn.close()

# Affichage des résultats
print("\nNombre d'épisodes diffusés par pays en Octobre:")
for country, count in country_counts:
    print(f"{country}: {count} épisodes")

# Écriture des résultats dans le fichier README.md
with open("README.md", "a") as readme:
    readme.write("\n## Résultats d'analyse\n")
    readme.write("\nNombre d'épisodes diffusés par pays en Octobre:\n")
    for country, count in country_counts:
        readme.write(f"- {country}: {count} épisodes\n")
