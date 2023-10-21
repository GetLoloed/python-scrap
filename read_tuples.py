def read_episodes_csv(filename):
    # Ouvrir le fichier en mode lecture
    with open(filename, 'r', encoding='utf-8') as file:
        # Lire les lignes du fichier
        lines = file.readlines()

        # Retirer les espaces et séparer les éléments par le caractère ';'
        data = [line.strip().split(';') for line in lines]

        # Convertir les données au bon type
        formatted_data = []
        for row in data:
            serie_name = row[0]
            n_episode = int(row[1])
            n_saison = int(row[2])
            channel = row[3]
            country = row[4]
            h_ref = row[5]
            date = row[6]

            formatted_data.append((serie_name, n_episode, n_saison, channel, country, h_ref, date))

        return formatted_data


# Utilisation
filename = 'data/files/episodes.csv'
episodes = read_episodes_csv(filename)
print(episodes)
