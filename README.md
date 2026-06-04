# Minimal FastAPI Example

Application web minimaliste construite avec FastAPI. Elle combine un portfolio CV dynamique gérable depuis une interface admin.

## Fonctionnalités

- **Portfolio CV** — page publique affichant les informations du CV (profil, expériences, formations, compétences, projets, langues, centres d'intérêt, liens)
- **Interface admin** — modification du contenu du CV sans authentification via `/admin`
- **Documentation API** — interface Swagger automatique sur `/docs`

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Framework web | [FastAPI](https://fastapi.tiangolo.com/) |
| Base de données | SQLite via [SQLAlchemy](https://www.sqlalchemy.org/) |
| Templates HTML | [Jinja2](https://jinja.palletsprojects.com/) |
| Validation des données | [Pydantic v2](https://docs.pydantic.dev/) |
| Serveur | [Uvicorn](https://www.uvicorn.org/) |

## Installation

### 1. Prérequis

Python 3.10 ou supérieur. Vérifier avec :
```bash
python --version
```

### 2. Créer et activer un environnement virtuel

```bash
# Créer l'environnement
python -m venv .venv

# Activer (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activer (Linux / macOS)
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

```bash
python app/main.py
```

L'application est accessible sur **http://localhost:8000**.

## Pages disponibles

| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Portfolio CV public |
| `http://localhost:8000/admin` | Interface d'administration du CV |
| `http://localhost:8000/docs` | Documentation interactive de l'API (Swagger UI) |



## Structure du projet

```
minimal_fastapi_example/
│
├── app/
│   ├── main.py                      # Point d'entrée, configuration FastAPI
│   │
│   ├── core/
│   │   └── database.py              # Connexion SQLite, Base SQLAlchemy, get_db()
│   │
│   ├── models/
│   │   ├── cv_section.py            # Modèle ORM : table cv_sections
│   │   └── measurement.py           # Modèle ORM : table measurements
│   │
│   ├── schemas/
│   │   ├── cv_section_schema.py     # Schémas Pydantic pour le CV (Create, Update)
│   │   └── measurement_schema.py    # Schémas Pydantic pour les mesures
│   │
│   ├── crud/
│   │   ├── cv_section_crud.py       # Opérations CRUD sur les sections de CV
│   │   └── measurement_crud.py      # Opérations CRUD sur les mesures
│   │
│   ├── routers/
│   │   ├── cv_router.py             # Routes portfolio et admin
│   │   └── measurement_router.py    # Routes API mesures
│   │
│   └── templates/
│       ├── portfolio.html           # Page CV publique
│       ├── admin.html               # Interface d'administration
│       └── admin_edit.html          # Formulaire de modification d'une section
│
├── static/
│   └── photos/                      # Images servies statiquement
│
├── tests/
│   ├── conftest.py                  # Fixtures pytest (base de données en mémoire)
│   └── test_cv_crud.py              # Tests unitaires du CRUD CV
│
├── requirements.txt                 # Dépendances Python
└── conftest.py                      # Configuration pytest (ajout de app/ au sys.path)
```

## Base de données

SQLite, fichier créé automatiquement au premier démarrage : `app/localdb.sqlite3`.

### Table `cv_sections`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER | Clé primaire, auto-incrémentée |
| `section_type` | TEXT | Type : `about`, `experience`, `formation`, `skill`, `project`, `language`, `interest`, `link` |
| `title` | TEXT | Titre principal de l'entrée |
| `subtitle` | TEXT | Sous-titre optionnel (entreprise, école, niveau…) |
| `description` | TEXT | Texte libre optionnel |
| `order` | INTEGER | Ordre d'affichage au sein du même type |
| `extra` | TEXT | Champs additionnels sérialisés en JSON (dates, URL, niveau…) |


## Lancer les tests

```bash
pytest tests/ -v
```

