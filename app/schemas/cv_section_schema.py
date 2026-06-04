from pydantic import BaseModel
from typing import Optional


class CvSectionCreate(BaseModel):
    """Données nécessaires pour créer une nouvelle section de CV.

    Utilisé dans les formulaires admin (POST /admin/sections) et le script de seed.
    """

    section_type: str           # Type de section : about, experience, formation, skill, project, language, interest, link
    title: str                  # Titre principal (obligatoire)
    subtitle: Optional[str] = None      # Sous-titre optionnel
    description: Optional[str] = None  # Texte libre optionnel
    order: int = 0                      # Ordre d'affichage (0 = premier)
    extra: Optional[str] = None         # JSON sérialisé avec les champs spécifiques au type


class CvSectionUpdate(BaseModel):
    """Données pour modifier une section existante.

    Tous les champs sont optionnels : seuls les champs fournis sont mis à jour
    (grâce à model_dump(exclude_unset=True) dans le CRUD).
    """

    title: Optional[str] = None
    subtitle: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    extra: Optional[str] = None
