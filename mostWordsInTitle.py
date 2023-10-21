import os
import sqlite3
from collections import Counter
import re

# Établir la connexion avec la base de données SQLite
path = 'data/databases'
conn = sqlite3.connect(os.path.join(path, 'database.db'))
cursor = conn.cursor()

cursor.execute("""
SELECT serie_name
FROM episode
""")
series_names = cursor.fetchall()
conn.close()

# Calcul des 10 mots les plus courants dans les noms de séries
words = []
for (name,) in series_names:
    words.extend(re.findall(r'\w+', name))

word_counts = Counter(words)
most_common_words = word_counts.most_common(10)

# Affichage des résultats
print("\nLes 10 mots les plus présents dans les noms des séries:")
for word, count in most_common_words:
    print(f"{word}: {count}")
