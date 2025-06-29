from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker 
# declarative_base est utilisé pour  créer des modèles de données
# sessionmaker est utilisé pour créer des sessions de base de données


engine = create_engine('postgresql://postgres:passerpasser@localhost:5432/pizza_db', echo=True) 

# echo=True pour afficher les requêtes SQL dans la console
# echo=False pour ne pas afficher les requêtes SQL

Base = declarative_base()  # Classe de base pour les modèles de données
Session=sessionmaker()  # Classe pour créer des sessions de base de données