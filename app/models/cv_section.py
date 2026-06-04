from sqlalchemy import Column, String, Integer, Text
from app.core.database import Base


class CvSection(Base):
    """Représente une section du CV dans la base de données.

    Chaque entrée correspond à un bloc d'information affiché sur le portfolio :
    profil, expérience, formation, compétence, projet, langue, intérêt ou lien.

    Le champ `extra` stocke un JSON dont la structure varie selon `section_type` :
        - about      : {"email": str, "location": str}
        - experience : {"date_start": str, "date_end": str, "location": str}
        - formation  : {"date_start": str, "date_end": str}
        - skill      : {"level": int (0-100)}
        - project    : {"url": str, "github": str}
        - link       : {"url": str}
    """

    __tablename__ = "cv_sections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    section_type = Column(String(50), nullable=False)   # about | experience | formation | skill | project | language | interest | link
    title = Column(String(200), nullable=False)          # Titre principal de l'entrée
    subtitle = Column(String(200), nullable=True)        # Sous-titre optionnel (entreprise, école, niveau…)
    description = Column(Text, nullable=True)            # Texte libre
    order = Column(Integer, nullable=False, default=0)   # Ordre d'affichage au sein d'un même type
    extra = Column(String, nullable=True)                # Données additionnelles sérialisées en JSON

    def __str__(self):
        return f"[{self.section_type}] {self.title}"
