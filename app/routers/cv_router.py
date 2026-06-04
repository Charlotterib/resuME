"""Routes liées au portfolio CV et à son interface d'administration.

Routes exposées :
    GET  /                              → Page portfolio publique
    GET  /admin                         → Interface d'administration (sans authentification)
    POST /admin/sections                → Créer une section
    GET  /admin/sections/{id}/edit      → Formulaire de modification
    POST /admin/sections/{id}/edit      → Enregistrer les modifications
    POST /admin/sections/{id}/delete    → Supprimer une section
"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.crud import cv_section_crud as crud
from app.core.database import get_db
from collections import defaultdict
from urllib.parse import urlencode
import json

router = APIRouter(tags=["CV"])
templates = Jinja2Templates(directory="app/templates")


def _parse_extra(section):
    """Ajoute l'attribut `extra_dict` à une instance CvSection.

    Le champ `extra` est stocké en JSON dans la base. Cette fonction le
    désérialise et l'attache directement à l'objet pour faciliter l'accès
    dans les templates Jinja2 (ex: section.extra_dict.get('email')).

    Args:
        section: Instance CvSection issue de SQLAlchemy.

    Returns:
        La même instance, avec `extra_dict` (dict) ajouté dynamiquement.
    """
    section.extra_dict = json.loads(section.extra) if section.extra else {}
    return section


def _group_sections(sections: list) -> dict:
    """Regroupe les sections par type et les trie par ordre d'affichage.

    Args:
        sections: Liste de CvSection avec `extra_dict` attaché.

    Returns:
        Dictionnaire { section_type: [CvSection, ...] } trié par `order`.
    """
    grouped = defaultdict(list)
    for s in sections:
        grouped[s.section_type].append(s)
    for key in grouped:
        grouped[key].sort(key=lambda x: x.order)
    return dict(grouped)


def _build_extra(section_type: str, extra_email: str, extra_location: str,
                 extra_date_start: str, extra_date_end: str, extra_level: str,
                 extra_url: str, extra_github: str) -> str | None:
    """Construit la chaîne JSON `extra` à partir des champs de formulaire.

    Chaque type de section utilise un sous-ensemble des champs disponibles.
    Les types non reconnus (language, interest) retournent None.

    Args:
        section_type: Type de la section (about, experience, skill…).
        extra_email, extra_location, extra_date_start, extra_date_end,
        extra_level, extra_url, extra_github: Valeurs des champs du formulaire.

    Returns:
        Chaîne JSON ou None si le type n'a pas de champs extra.
    """
    mapping = {
        "about": {"email": extra_email, "location": extra_location},
        "experience": {"date_start": extra_date_start, "date_end": extra_date_end, "location": extra_location},
        "formation": {"date_start": extra_date_start, "date_end": extra_date_end},
        "skill": {"level": int(extra_level) if extra_level and extra_level.isdigit() else 0},
        "project": {"url": extra_url, "github": extra_github},
        "link": {"url": extra_url},
    }
    data = mapping.get(section_type)
    return json.dumps(data) if data is not None else None


# ── Page principale ───────────────────────────────────────────────────────────

@router.get("/")
async def portfolio(request: Request, db: Session = Depends(get_db)):
    """Affiche la page portfolio publique.

    Appelle seed_about() pour garantir l'existence d'un profil par défaut
    si la base est vide, puis récupère et regroupe toutes les sections.
    """
    crud.seed_about(db)
    sections = [_parse_extra(s) for s in crud.get_all_cv_sections(db)]
    grouped = _group_sections(sections)
    return templates.TemplateResponse(request, "portfolio.html", {
        "about": grouped.get("about", [None])[0],
        "experiences": grouped.get("experience", []),
        "formations": grouped.get("formation", []),
        "skills": grouped.get("skill", []),
        "projects": grouped.get("project", []),
        "languages": grouped.get("language", []),
        "interests": grouped.get("interest", []),
        "links": grouped.get("link", []),
    })


# ── Admin — liste ─────────────────────────────────────────────────────────────

@router.get("/admin")
async def admin(request: Request, db: Session = Depends(get_db), message: str = ""):
    """Affiche l'interface d'administration du CV.

    Args:
        message: Message flash affiché après une action (ajout, modification,
                 suppression). Passé en query string depuis les redirections.
    """
    sections = [_parse_extra(s) for s in crud.get_all_cv_sections(db)]
    grouped = _group_sections(sections)
    return templates.TemplateResponse(request, "admin.html", {
        "sections": grouped,
        "message": message,
    })


# ── Admin — créer ─────────────────────────────────────────────────────────────

@router.post("/admin/sections")
async def create_section(
    db: Session = Depends(get_db),
    section_type: str = Form(...),
    title: str = Form(...),
    subtitle: str = Form(""),
    description: str = Form(""),
    order: int = Form(0),
    extra_email: str = Form(""),
    extra_location: str = Form(""),
    extra_date_start: str = Form(""),
    extra_date_end: str = Form(""),
    extra_level: str = Form(""),
    extra_url: str = Form(""),
    extra_github: str = Form(""),
):
    """Crée une nouvelle section à partir des données du formulaire admin.

    Redirige vers /admin avec un message de confirmation (pattern POST-Redirect-GET).
    """
    from app.schemas.cv_section_schema import CvSectionCreate
    extra = _build_extra(section_type, extra_email, extra_location,
                         extra_date_start, extra_date_end, extra_level,
                         extra_url, extra_github)
    crud.create_cv_section(db, CvSectionCreate(
        section_type=section_type,
        title=title,
        subtitle=subtitle or None,
        description=description or None,
        order=order,
        extra=extra,
    ))
    return RedirectResponse(url="/admin?" + urlencode({"message": "Section ajoutée"}), status_code=303)


# ── Admin — formulaire d'édition ──────────────────────────────────────────────

@router.get("/admin/sections/{section_id}/edit")
async def edit_section_form(section_id: int, request: Request, db: Session = Depends(get_db)):
    """Affiche le formulaire de modification d'une section existante.

    Redirige vers /admin si la section est introuvable.
    """
    section = crud.get_cv_section_by_id(db, section_id)
    if not section:
        return RedirectResponse(url="/admin", status_code=303)
    return templates.TemplateResponse(request, "admin_edit.html", {"section": _parse_extra(section)})


# ── Admin — enregistrer l'édition ────────────────────────────────────────────

@router.post("/admin/sections/{section_id}/edit")
async def update_section(
    section_id: int,
    db: Session = Depends(get_db),
    title: str = Form(...),
    subtitle: str = Form(""),
    description: str = Form(""),
    order: int = Form(0),
    extra_email: str = Form(""),
    extra_location: str = Form(""),
    extra_date_start: str = Form(""),
    extra_date_end: str = Form(""),
    extra_level: str = Form(""),
    extra_url: str = Form(""),
    extra_github: str = Form(""),
):
    """Enregistre les modifications d'une section existante.

    Redirige vers /admin si la section est introuvable.
    Redirige vers /admin avec message de confirmation après la mise à jour.
    """
    section = crud.get_cv_section_by_id(db, section_id)
    if not section:
        return RedirectResponse(url="/admin", status_code=303)
    from app.schemas.cv_section_schema import CvSectionUpdate
    extra = _build_extra(section.section_type, extra_email, extra_location,
                         extra_date_start, extra_date_end, extra_level,
                         extra_url, extra_github)
    crud.update_cv_section(db, section, CvSectionUpdate(
        title=title,
        subtitle=subtitle or None,
        description=description or None,
        order=order,
        extra=extra,
    ))
    return RedirectResponse(url="/admin?" + urlencode({"message": "Section modifiée"}), status_code=303)


# ── Admin — supprimer ─────────────────────────────────────────────────────────

@router.post("/admin/sections/{section_id}/delete")
async def delete_section(section_id: int, db: Session = Depends(get_db)):
    """Supprime une section par son identifiant.

    Redirige vers /admin avec message de confirmation.
    """
    section = crud.get_cv_section_by_id(db, section_id)
    if section:
        crud.delete_cv_section(db, section)
    return RedirectResponse(url="/admin?" + urlencode({"message": "Section supprimée"}), status_code=303)
