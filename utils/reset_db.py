import psycopg2

database_url = "postgres://python_lc_6018:07YnJl1pnzwRx6xXhuHU@python-lc-6018.postgresql.a.osc-fr1.scalingo-dbs.com:32795/python_lc_6018?sslmode=prefer"

try:
    conn = psycopg2.connect(database_url, sslmode='prefer')
    cursor = conn.cursor()

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cursor.fetchall()

    # Supprimer toutes les tables
    for table in tables:
        table_name = table[0]
        drop_table_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
        cursor.execute(drop_table_query)
        print(f"Table '{table_name}' supprimée avec succès.")

    conn.commit()

    conn.close()

    print("Toutes les tables ont été supprimées avec succès.")
except psycopg2.Error as e:
    print(f"Une erreur s'est produite lors de la connexion à la base de données : {e}")
