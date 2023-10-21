# Sommaire

1. [Choix de Code Expliqués](#choix-de-code-expliqués)
2. [Consigne et Importance](#consigne-et-importance)
3. [Fichiers](#fichiers)
    - [episodes.py](#episodespy)
    - [episodes.csv](#episodescsv)
    - [episodesToCSV.py](#episodestocsvpy)
    - [insertInScalingo.py](#insertinscalingopy)
    - [insertInSqLite.py](#insertinsqlitepy)
    - [mostEpisodesByChannels.py](#mostepisodesbychannelspy)
    - [mostEpisodesByCountry.py](#mostepisodesbycountrypy)
    - [mostWordsInTitle.py](#mostwordsintitlepy)
    - [readTuple.py](#readtuplepy)
    - [summarize_episodes.py](#summarize_episodespy)
4. [Résultats d'analyse](#résultats-danalyse)
    - [Par chaîne de télévision](#par-chaîne-de-télévision)
    - [Par pays](#par-pays)

# Choix de Code Expliqués

Au cours de la réalisation de ce TP, des décisions stratégiques ont été prises pour optimiser le processus :

- **Organisation en fichiers distincts :**
    - Chaque exercice du TP est contenu dans un fichier dédié.
    - Avantages : Organisation claire, facilité de navigation, et modularité du TP.

- **Emploi de BeautifulSoup :**
    - Utilisé pour le scraping des pages web.
    - Raison : Sa robustesse et simplicité d'usage.

- **Adoption des expressions régulières :**
    - Servent à extraire des données de manière précise.
    - Contexte : Capturer des détails spécifiques des séries.

Ces décisions ont été prises pour garantir un code bien structuré, efficace tout en étant facilement compréhensible et adaptable.

# Consigne et Importance
## Consigne : "Pensez à bien utiliser cette commande dans le même terminal que celui que vous utilisez pour exécuter vos fichiers .py."
### Pourquoi c'est important :
Utiliser la même instance de terminal assure la cohérence de l'environnement. Cela garantit que toutes les configurations, variables d'environnement et contextes applicables à votre script Python sont maintenus et accessibles. Ignorer cette consigne peut entraîner des erreurs imprévues ou des comportements incohérents de votre script.

# Fichiers

- `episodes.py`: Script Python pour récupérer les données
- `episodes.csv`: Données récupérées
- `episodesToCSV.py`: Script Python pour convertir les données en CSV
- `insertInScalingo.py`: Script Python pour insérer les données dans la base de données
- `insertInSqLite.py`: Script Python pour insérer les données dans la base de données
- `mostEpisodesByChannels.py`: Script Python pour analyser les données
- `mostEpisodesByCountry.py`: Script Python pour analyser les données
- `mostWordsInTitle.py`: Script Python pour analyser les données
- `readTuple.py`: Script Python pour lire les données
- `summarize_episodes.py`: Script Python pour analyser les données

## Résultats d'analyse

### Par chaîne de télévision:

- Netflix: 108 épisodes
- Disney+: 34 épisodes
- Prime Video: 27 épisodes

### Par pays:

- Etats-Unis: 355 épisodes
- France: 76 épisodes
- Canada: 63 épisodes
- Royaume-Uni: 34 épisodes
- Allemagne: 16 épisodes
- Espagne: 14 épisodes
- Suède: 13 épisodes
- Corée du Sud: 6 épisodes
- Belgique: 3 épisodes
- Europe: 1 épisodes
- Danemark: 1 épisodes
- Australie: 1 épisodes
