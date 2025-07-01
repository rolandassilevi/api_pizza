# Pydantic utilisé pour la validation des données d'authentification
# Pydantic est un sérialiseur de données qui permet de valider et de sérialiser les données d'entrée et de sortie.
#import os
from pydantic import BaseModel
#from pydantic_settings import BaseSettings
from typing import Optional

class InscriptionModel(BaseModel):
    id : Optional[int]
    nom : str
    email : str
    password : str
    est_staff : Optional[bool] = False
    est_actif : Optional[bool] = True
    
    class Config:
        orm_mode = True 
        schema_extra = {                  
        #Exemple de données pour la documentation (Swagger UI)
            "example": {
                "nom": "John Doe",
                "email": "jonhdoe@johndoe.com",
                "password": "password123",
                "est_staff": False,
                "est_actif": True
            }
        }
    
    
        """
    model_config = {
        "from_attributes" : True, # orm_mode = True (ancienne syntaxe de Pydantic v1)
        "json_schema_extra" : { # schema_extra = {} (ancienne syntaxe de Pydantic v1)                   
        #Exemple de données pour la documentation (Swagger UI)
            "example": {
                "nom": "John Doe",
                "email": "jonhdoe@johndoe.com",
                "password": "password123",
                "est_staff": False,
                "est_actif": True
            }
        }
    }

        """

# "0c402bb9847bd3ac09f68da2e0e2e721fd7780423279cc92bbed7f17f04df998"
# os.getenv("JWT_SECRET", "valeur_par_defaut")

class Parametres(BaseModel):
    # secret_key: str =
    authjwt_secret_key: str = "0c402bb9847bd3ac09f68da2e0e2e721fd7780423279cc92bbed7f17f04df998" # Clé secrète pour JWT (JSON Web Token), généré par la commande secrets.token_hex() dans l'invite de commande Python

class ConnexionModel(BaseModel):
    nom: str
    password: str
    
class CommandeModel(BaseModel):
    id : Optional[int]
    quantite : int
    statut_commande : Optional[str]="EN_ATTENTE"
    taille_pizza : Optional[str]="PETITE"
    id_utilisateur : Optional[int]
    
    class Config:
        orm_mode = True 
        schema_extra = {                  
        #Exemple de données pour la documentation (Swagger UI)
            "example": {
                "quantite": 1,
                "taille_pizza": "PETITE"
            }
        }
        
class CommandeStatutModel(BaseModel):
    statut_commande: Optional[str] = "EN_ATTENTE"

    class Config:
        orm_mode = True 
        schema_extra = {                  
        #Exemple de données pour la documentation (Swagger UI)
            "example": {
                "statut_commande" : "EN_LIVRAISON"
            }
        }
