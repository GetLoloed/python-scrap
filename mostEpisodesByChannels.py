import os
import sqlite3

# Établir la connexion avec la base de données SQLite
path = 'data/databases'
conn = sqlite3.connect(os.path.join(path, 'database.db'))
cursor = conn.cursor()

cursor.execute("""
SELECT channel, COUNT(channel) as count
FROM episode
GROUP BY channel
ORDER BY count DESC
""")
channel_counts = cursor.fetchall()
conn.close()

# Affichage des résultats
print("\nNombre d'épisodes diffusés par chaîne de télévision en Octobre:")
for channel, count in channel_counts:
    print(f"{channel}: {count} épisodes")

# Écriture des résultats dans le fichier README.md
with open("README.md", "a") as readme:
    readme.write("\n## Résultats d'analyse\n")
    readme.write("\nNombre d'épisodes diffusés par chaîne de télévision en Octobre:\n")
    for channel, count in channel_counts:
        readme.write(f"- {channel}: {count} épisodes\n")
