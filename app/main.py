"""Point d'entrée de l'application FastAPI.

 

L'application expose :
    - Un portfolio CV public sur GET /
    - Une interface admin sur GET /admin
    - Une API REST pour les mesures de capteurs sur /measurements
    - La documentation Swagger sur /docs
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from app.core.database import create_db
from app.routers import cv_router

app = FastAPI(title="Minimal Fastapi Example", docs_url="/docs")

# Fichiers statiques servis directement (images, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Création des tables en base si elles n'existent pas encore
create_db()

#app.include_router(measurement_router.router)
app.include_router(cv_router.router)

if __name__ == "__main__":
        uvicorn.run(app, host="localhost", port=8000)
