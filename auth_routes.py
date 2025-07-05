from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from database import Session, engine
from schemas import InscriptionModel, ConnexionModel
from models import Utilisateur
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash # werkzeug.security pour le hachage du mot de passe (utilisé par Flask, mais aussi utile pour la sécurité et les requêtes HTTP)
from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.encoders import jsonable_encoder # Pour encoder les données (dictionnaire) en JSON


# ----------------------------------------------------------------
# Routeur dédié à l’authentification : préfixe /auth et tag "auth"
# ----------------------------------------------------------------
auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

session = Session(bind=engine)

""" 
# Exemple de route non protégée (sans AuthJWT)
# Pour tester l'authentification, vous pouvez utiliser cette route pour vérifier que le routeur fonctionne correctement.
# Vous pouvez accéder à cette route sans authentification.

@auth_router.get("/")
async def hello():
    return {"message": "Hello de *auth router!*"}
"""

# Exemple de route protégée (avec AuthJWT)
# Pour tester l'authentification, vous pouvez utiliser cette route pour vérifier que le routeur fonctionne correctement.
# Vous devez fournir un token JWT valide dans l'en-tête Authorization pour accéder à cette route.
# Si le token est invalide ou manquant, une exception HTTP 401 sera levée.

@auth_router.get("/")
# async def hello():
async def hello(Authorize: AuthJWT = Depends()):
    #Protéger la route avec AuthJWT
    """
        ## Routes pour authentification et inscription
        Test de la route d'authentification.
        Ceci est une route de test pour vérifier que le routeur fonctionne correctement.
        Vous devez fournir un token JWT valide dans l'en-tête Authorization pour accéder à cette route.
        Si le token est invalide ou manquant, une exception HTTP 401 sera levée.
        
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    return {"message": "Hello de *auth router!*"}

@auth_router.post("/inscription", status_code=status.HTTP_201_CREATED) # "/inscription", response_model=InscriptionModel, status_code=status.HTTP_201_CREATED -> Internal Server Error (500) si le modèle n'est pas correctement défini
async def inscription(utilisateur: InscriptionModel):
    """
        ## Route pour l'inscription d'un nouvel utilisateur
        Créer un nouvel utilisateur.
        
        Informations nécessaires
        
        ``` 
        nom: str
        email: str 
        password: str
        est_staff: bool 
        est_actif: bool          
        ```

    """
   
    db_email = session.query(Utilisateur).filter(Utilisateur.email == utilisateur.email).first() # Vérification de l'existance de l'email (l'unicité de l'email)
    if db_email is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'email est déjà utilisé pour un Utilisateur."
        )
        
    db_nom = session.query(Utilisateur).filter(Utilisateur.nom == utilisateur.nom).first() # Vérification de l'existance du nom (l'unicité du nom)
    if db_nom is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nom est déjà utilisé pour un Utilisateur."
        )
        
    # Création d'un nouvel utilisateur
    nouvel_utilisateur = Utilisateur(
        nom=utilisateur.nom,
        email=utilisateur.email,
        password=generate_password_hash(utilisateur.password),  # Hachage du mot de passe (grâce à werkzeug)
        est_staff=utilisateur.est_staff,
        est_actif=utilisateur.est_actif
    )
    
    session.add(nouvel_utilisateur)
    session.commit()
    
    return nouvel_utilisateur

# Route Connexion
@auth_router.post("/connexion", status_code=200)
async def connexion(utilisateur: ConnexionModel, Authorize: AuthJWT = Depends()):
    
    """
        ## Route pour la connexion d'un utilisateur
                
        Informations nécessaires
        
        ``` 
        nom: str
        password: str        
        ```
        Retourne un token d'accès `access` et un token de rafraîchissement `refresh` si les informations d'identification sont valides.
    """
    #pass
    db_utilisateur = session.query(Utilisateur).filter(Utilisateur.nom == utilisateur.nom).first()
    
    if db_utilisateur and check_password_hash(getattr(db_utilisateur, "password"), utilisateur.password): # utiliser getattr pour accéder à l'attribut password de l'objet db_utilisateur (getattr(db_utilisateur, "password")), au lieu de db_utilisateur.password
        access_token = Authorize.create_access_token(subject=getattr(db_utilisateur, "nom"))
        refrech_token = Authorize.create_refresh_token(subject=getattr(db_utilisateur, "nom"))
        
        reponse = {
            "access": access_token,
            "refresh": refrech_token,
        }
        
        return jsonable_encoder(reponse)  # Utilisation de jsonable_encoder pour encoder la réponse (dictionnaire) en JSON
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nom d'utilisateur ou mot de passe incorrect.")

# 25/06/2025
# Actualisation de tokens
@auth_router.get("/actualiser")
async def actualiser_token(Authorize: AuthJWT = Depends()):
    
    """
        ## Route créer un token d'accès actualisé
        
        Cette route permet de créer un nouveau token d'accès à partir d'un token de rafraîchissement valide.
        Vous devez fournir un token de rafraîchissement valide dans l'en-tête Authorization pour accéder à cette route.
        Si le token de rafraîchissement est invalide ou manquant, une exception HTTP 401 sera levée.
                
        Informations nécessaires
        
        ``` 
        nom: str
        password: str        
        ```
    """
    
    try:
        Authorize.jwt_refresh_token_required()
        #current_user = Authorize.get_jwt_subject()
        #new_access_token = Authorize.create_access_token(subject=current_user)
        #return {"access_token": new_access_token}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Veuillez fournir un token actualisé valide.")
    
    utilisateur_actuel = Authorize.get_jwt_subject()  # Récupère l'identité de l'utilisateur à partir du token JWT
    
    # Si le token est valide, crée un nouveau token d'accès
    access_token = Authorize.create_access_token(subject=utilisateur_actuel) # type: ignore
    
    return jsonable_encoder({"access": access_token})  # Utilisation de jsonable_encoder pour encoder la réponse (dictionnaire) en JSON