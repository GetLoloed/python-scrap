import psycopg2

# Connexion à la base de données PostgreSQL sur Scalingo
DATABASE_URL = "postgres://python_lc_6018:07YnJl1pnzwRx6xXhuHU@python-lc-6018.postgresql.a.osc-fr1.scalingo-dbs.com:32795/python_lc_6018?sslmode=prefer"
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Sélectionner toutes les données de la table 'episode'
select_query = "SELECT * FROM episode;"
cursor.execute(select_query)

# Récupérer toutes les lignes de résultats
rows = cursor.fetchall()

# Afficher le nombre de lignes dans la table
print(f"Nombre de lignes dans la table 'episode': {len(rows)}")

# Afficher les données
for row in rows:
    print(row)

# Fermer la connexion
conn.close()
