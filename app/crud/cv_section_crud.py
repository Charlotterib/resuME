from sqlalchemy.orm import Session
from app.models.cv_section import CvSection
from app.schemas.cv_section_schema import CvSectionCreate, CvSectionUpdate


def create_cv_section(db: Session, data: CvSectionCreate) -> CvSection:
    """Insère une nouvelle section dans la base de données.

    Args:
        db: Session SQLAlchemy active.
        data: Données validées de la nouvelle section.

    Returns:
        L'objet CvSection créé, rafraîchi depuis la base.
    """
    section = CvSection(**data.model_dump())
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


def get_all_cv_sections(db: Session) -> list[CvSection]:
    """Retourne toutes les sections de CV, sans filtre ni tri.

    Args:
        db: Session SQLAlchemy active.

    Returns:
        Liste de tous les objets CvSection.
    """
    return db.query(CvSection).all()


def get_cv_sections_by_type(db: Session, section_type: str) -> list[CvSection]:
    """Retourne toutes les sections d'un type donné.

    Args:
        db: Session SQLAlchemy active.
        section_type: Type de section (ex: "skill", "experience").

    Returns:
        Liste des CvSection correspondant au type.
    """
    return db.query(CvSection).filter(CvSection.section_type == section_type).all()


def get_cv_section_by_id(db: Session, section_id: int) -> CvSection | None:
    """Retourne une section par son identifiant.

    Args:
        db: Session SQLAlchemy active.
        section_id: Identifiant de la section.

    Returns:
        L'objet CvSection correspondant, ou None si introuvable.
    """
    return db.query(CvSection).filter(CvSection.id == section_id).first()


def update_cv_section(db: Session, section: CvSection, data: CvSectionUpdate) -> CvSection:
    """Met à jour les champs d'une section existante.

    Seuls les champs explicitement renseignés dans `data` sont modifiés.

    Args:
        db: Session SQLAlchemy active.
        section: L'objet CvSection à modifier.
        data: Champs à mettre à jour.

    Returns:
        L'objet CvSection mis à jour.
    """
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(section, field, value)
    db.commit()
    db.refresh(section)
    return section


def delete_cv_section(db: Session, section: CvSection) -> CvSection:
    """Supprime une section de la base de données.

    Args:
        db: Session SQLAlchemy active.
        section: L'objet CvSection à supprimer.

    Returns:
        L'objet supprimé (plus disponible en base).
    """
    db.delete(section)
    db.commit()
    return section


def seed_about(db: Session):
    """Crée une entrée 'about' par défaut si la base est vide.

    Appelé au démarrage de chaque requête GET / pour garantir que la page
    portfolio affiche toujours quelque chose, même sans données saisies.
    """
    if get_all_cv_sections(db) == []:
        create_cv_section(db, CvSectionCreate(
            section_type="about",
            title="Votre nom",
            subtitle="Votre rôle",
            order=0,
            extra='{"email": "", "location": ""}',
        ))
