# Minimal FastAPI Example

Portfolio construit avec FastAPI. Il s'agit d'un portfolio CV dynamique qu'on peut gérer depuis l'admin.

## Fonctionnalités

- **Portfolio CV** — page publique affichant les informations du CV (profil, expériences, formations, compétences, projets, langues, centres d'intérêt, liens)
- **Interface admin** — modification du contenu du CV sans authentification via `/admin`
- **Documentation API** — interface Swagger automatique sur `/docs`

## Partie technique

API Web : FastAPI
Base de Données : SQLite avec l'outil SQLAlchemy
Templates HTML : Jinja2
Serveur : Uvicorn

## Installation et Lancement

```bash
#Clone le repo
git clone https://github.com/Charlotterib/resuME
# Créer l'environnement
python -m venv .venv

# Activer 
.venv\Scripts\Activate.ps1
```

```bash
#dépendences
pip install -r requirements.txt
```

```bash
#lancement du serveur
uvicorn app.main:app --host localhost --port 8000 --reload
```

L'application est accessible sur **http://localhost:8000**.

## Pages disponibles

 `http://localhost:8000/`  Portfolio CV public 
 `http://localhost:8000/admin`  Interface d'administration du CV 
 `http://localhost:8000/docs`  Documentation interactive de l'API (Swagger UI) 



### Table `cv_sections`

Cette table contient toutes les informations du portfolio. Chaque ligne correspond à une section du CV (profil, expérience, formation, compétence, projet, etc.).

- **id** *(INTEGER)* : identifiant unique de la section, généré automatiquement (clé primaire).
- **section_type** *(VARCHAR(50))* : type de la section (`about`, `experience`, `formation`, `skill`, `project`, `language`, `interest` ou `link`).
- **title** *(VARCHAR(200))* : titre principal affiché sur le portfolio.
- **subtitle** *(VARCHAR(200))* : sous-titre optionnel (entreprise, école, niveau, etc.).
- **description** *(TEXT)* : description détaillée de la section.
- **order** *(INTEGER)* : ordre d'affichage des éléments appartenant à un même type de section.
- **extra** *(TEXT)* : informations supplémentaires stockées au format JSON (dates, localisation, niveau de compétence, URL, GitHub, etc.).

Le champ **extra** permet de stocker des données différentes selon le type de section sans avoir besoin d'ajouter de nouvelles colonnes à la table.