from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#pour récuperer l'url de la base ( path du fichier physique)
SQLALCHEMY_DATABASE_URL = "sqlite:///app/localdb.sqlite3"

# create_engine est un outil de base de donnée, il fait le lien en l'app et la db
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True,
    connect_args={"check_same_thread": False}
)


# session local va gérer les sessions d'utilisation de la databse, une session = une connexion a la db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base est la classe mère des modeles, les sous-classes qui en héritent seront bien prises par l'outil SQLAlchemy comme des tables SQL
Base = declarative_base()

def create_db():
    # Tous les modèles créés depuis la Base sont transformés en tables SQL si elles n'existent pas déjà
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Cette fonction est utilisée pour ouvrir une database session lorsqu'une fonction qui a besoin de la database l'appelle ,
    Puis la refermer à la fin de l'appel de fonction. Elle permet de gérer proprement les connections avec la database
    On ouvre la connexion, puis lecture/ecriture, on valide et on referme
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Ensures the database session is always closed, even if exceptions occur.