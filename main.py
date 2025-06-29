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

@AuthJWT.load_config # type: ignore # Supprime l'avertissement de type, car Pylance infère mal le type d’annotation dans cette version du paquet fastapi-jwt-auth
def get_config():
    return Parametres()

app.include_router(auth_router)
app.include_router(order_router)
