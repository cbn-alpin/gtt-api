# gtt-api
Backend de l'outil de Gestion du Temps de Travail (GTT).

Installation et utilisation

⚠️ Attention, le projet fonctionne uniquement sous Python v3.x

Pour installer ce projet :

Cloner le projet dans votre "workspace" local :

    git clone https://github.com/cbn-alpin/gtt-api.git

Se deplacer dans le dossier du projet cloné :

    cd gtt-api/

Créer un environnement virtuel :

    python -m venv cbna_env

Activer l'environnement virtuel :

    ./cbna_env/bin/activate

Installer les dépendances :

    pip install -r requirements.txt


Lancement du framwork Flask :

    FLASK_APP=src/main.py flask run
