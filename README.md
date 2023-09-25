version = 0.0.5
## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`


## Déploiement
### CICD

Pour le CI/CD, actuellement il s'agit de CircleCI.
#### CircleCI

Le fichier de configuration du pipeline (./.circleci/config.yml) contient 3 jobs :

1. Le job de test, qui installe les dépendances et exécute les tests.
2. Le job de build, qui construit l'image Docker et la pousse sur le Docker Hub.
3. Le job de déploiement, qui déploie l'application en production.

Pour le job de build, il faut ajouter les variables d'environnement suivantes sur CircleCI :

- DOCKERHUB_USERNAME
- DOCKERHUB_PASSWORD

> [!NOTE]
> Il faudra modifier si besoin le nom du repo Docker ici "oc-lettings-site" !

Pour le job de déploiement, il faut ajouter les variables d'environnement suivantes sur CircleCI :

- HEROKU_APP_NAME
- HEROKU_API_KEY

Le job de déploiement exécute plusieurs commandes :

1. "Deploy to Heroku" qui déploie l'application sur Heroku.
2. "Wait deploy to heroku complete" qui s'assure que le serveur est bien démarré avant la suite.
3. "Migrations" qui exécute les migrations.
4. "Load dumped data" qui charge le dump de la base de données depuis le fichier ./dumped_data/data.json.

> [!IMPORTANT]
> S'il n'y a pas de dump à charger ou que l'on ne souhaite pas le charger, il faut penser à commenter le bloc "Load dumped data".

### Configuration du serveur de production
#### Variables d'environnement

Sur le serveur de production, il faut mettre en place quelques variables d'environnement :

- ENV = PRODUCTION
- DJANGO_SECRET_KEY = CLÉ_SECRÈTE_DE_PRODUCTION
- DATABASE_URL de la forme suivante : 'postgres://<utilisateur>:<mot_de_passe>@<adresse_du_serveur_de_base_de_données>/<nom_de_la_base_de_données>'

Pour utiliser un autre serveur de base de données que PostgreSQL, consultez la documentation suivante :

- [Documentation de Django](https://docs.djangoproject.com/en/3.0/ref/databases/)
- [Page PyPi de dj-database-url](https://pypi.org/project/dj-database-url/)

### Fichiers statiques et médias

Pour utiliser des fichiers statiques et des médias, on peut utiliser WhiteNoise ou mettre en place une autre solution.

Pour utiliser une autre solution, il faut modifier ces deux lignes dans le fichier de settings de production.

- `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`
- `MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']`