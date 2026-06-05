"""Fichier principal permettant de lancer l'application.

 

L'application contient :
    - Un portfolio CV public sur GET /
    - Une interface admin sur GET /admin
    - La documentation Swagger sur /docs
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from app.core.database import create_db
from app.routers import cv_router

#pour créer le serveur web, app sera ensuite utilisée par uvicorn
app = FastAPI(title="Charlotte and Camille's Portfolio", docs_url="/docs")

# Permet de mount ("récuperer") tous les fichiers static (photos,css...)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Création de la base de données si elle n'existe pas encore
create_db()

#ajout de la route cv 
app.include_router(cv_router.router)

if __name__ == "__main__":
        uvicorn.run(app, host="localhost", port=8000)
        #permet de lancer l'application sur un port d'un ordi pour héberger le site localement