from sqlalchemy.orm import Session
from app.models.cv_section import CvSection
from app.schemas.cv_section_schema import CvSectionCreate, CvSectionUpdate


def create_cv_section(db: Session, data: CvSectionCreate) -> CvSection:
    """Pour insérer une nouvelle section dans le portfolio, ce qui veut dire un modèle hérité de Base.
    Prend en entrée une session  SQL Alchemy et les données de la nouvelle section.
    En retour, la Section est créée dans la session, la session est "refresh" (mise à jour/prise en compte)

    """
    section = CvSection(**data.model_dump())
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


def get_all_cv_sections(db: Session) -> list[CvSection]:
    """
    Cette fonction retourne la liste toutes les sections du portfolio en prenant en entrée la session SQLAlchemy

    """
    return db.query(CvSection).all()


def get_cv_sections_by_type(db: Session, section_type: str) -> list[CvSection]:
    """
    Retourne toutes les sections d'un type donné : prend en entrée la section (ex : experience)
    Et retourne la liste  CVSection correspondant. Doit aussi prendre en entrée la session SQLALchemy

    """
    return db.query(CvSection).filter(CvSection.section_type == section_type).all()


def get_cv_section_by_id(db: Session, section_id: int) -> CvSection | None:
    """ même principe que fonction précédente mais en prenant l'id de la section en argument
    """
    return db.query(CvSection).filter(CvSection.id == section_id).first()


def update_cv_section(db: Session, section: CvSection, data: CvSectionUpdate) -> CvSection:
    """
    Met à jour les champs d'une section existante, seulement les éléments modifiés.
    Prends en entrée la session (toujours pour CRUD la db), la section et les champs à modifier.

    """
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(section, field, value)
    db.commit()
    db.refresh(section)
    return section


def delete_cv_section(db: Session, section: CvSection) -> CvSection:
    """Supprime une section de la base de données.
    même principe, en retour la section ne sera plus dans la base
    """
    db.delete(section)
    db.commit()
    return section


def seed_about(db: Session):
    """
    Si les tables sont vides (par ex : première utilisation de l'admin),
    Une première section 'about' est créé avec des valeurs avec des valeurs classiques, ex "votre nom"
    """
    if get_all_cv_sections(db) == []:
        create_cv_section(db, CvSectionCreate(
            section_type="about",
            title="Votre nom",
            subtitle="Votre rôle",
            order=0,
            extra='{"email": "", "location": ""}',
        ))
