from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from schemas import Parametres
from pydantic import BaseModel
#from pydantic_settings import BaseSettings

# ----------------------------------------------------------------
# Instanciation de l'application FastAPI
# ----------------------------------------------------------------
app = FastAPI()
"""
    API pour la gestion des commandes de pizzas
    Cette API permet aux utilisateurs de s'inscrire, de se connecter et de passer des commandes de pizzas.
    Elle utilise JWT (JSON Web Tokens) pour l'authentification et la sécurité des routes.
    Les utilisateurs peuvent également gérer leurs commandes (créer, lister, mettre à jour et supprimer).
    L'API est divisée en deux routeurs : un pour l'authentification et un pour les commandes.
"""

@AuthJWT.load_config # type: ignore # Supprime l'avertissement de type, car Pylance infère mal le type d’annotation dans cette version du paquet fastapi-jwt-auth
def get_config():
    return Parametres()

app.include_router(auth_router)
app.include_router(order_router)
