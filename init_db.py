from database import engine,Base
from models import Utilisateur,Commande

Base.metadata.create_all(bind=engine)  # Crée les tables dans la base de données