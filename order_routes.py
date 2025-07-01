from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import Utilisateur,Commande
from schemas import CommandeModel,CommandeStatutModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder  # Pour encoder les données (dictionnaire) en JSON
 
# ----------------------------------------------------------------
# Routeur dédié aux opérations sur les commandes (/commandes)
# ----------------------------------------------------------------
order_router = APIRouter(
    prefix="/commandes",
    tags=["commandes"]
)

session = Session(bind=engine)

@order_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    #Protéger la route avec AuthJWT
    """
        ## Routes pour les commandes
        Test de la route de commandes.
        Ceci est une route de test pour vérifier que le routeur fonctionne correctement.
        Vous devez fournir un token JWT valide dans l'en-tête Authorization pour accéder à cette route.
        Si le token est invalide ou manquant, une exception HTTP 401 sera levée.
    """
    # Vérifier si le token JWT est valide
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    
    return {"message": "Route de commandes Opérationnelle!"}

@order_router.post("/commande", status_code=status.HTTP_201_CREATED)
async def effectuer_commande(commande: CommandeModel, Authorize: AuthJWT = Depends()):
    # Protéger la route avec AuthJWT
    """
        ## Route pour effectuer une commande de pizza
        Informations nécessaires :
    - **quantite**: int - Quantité de pizzas à commander
    - **taille_pizza**: str - Taille de la pizza (PETITE, MOYENNE, GRANDE, FAMILIALE)
    - **id_utilisateur**: int - Identifiant de l'utilisateur qui effectue la commande (optionnel)
    """
    # Vérifier si le token JWT est valide
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    
    utilisateur_actuel = Authorize.get_jwt_subject()
    utilisateur = session.query(Utilisateur).filter(Utilisateur.nom == utilisateur_actuel).first()
    
    nouvelle_commande = Commande(
        quantite=commande.quantite,
        taille_pizza=commande.taille_pizza
    )
    
    nouvelle_commande.utilisateur = utilisateur
    session.add(nouvelle_commande)
    session.commit()
    
    reponse = {
        "taille_pizza": nouvelle_commande.taille_pizza,
        "quantite": nouvelle_commande.quantite,
        "id": nouvelle_commande.id,
        "statut_commande": nouvelle_commande.statut_commande,
    }
    
    return jsonable_encoder(reponse)  # Encode les données en JSON pour la réponse

@order_router.get("/commandes")
async def liste_commandes(Authorize : AuthJWT = Depends()):
    #Protéger la route avec AuthJWT
    """
        ## Route pour lister les commandes de pizza
        Lister toutes les commandes de pizza. Ceci est accessible uniquement aux Super-Utilisateurs (staff).
    
    """
    # Vérifier si le token JWT est valide
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    
    utilisateur_actuel = Authorize.get_jwt_subject()
    
    utilisateur = session.query(Utilisateur).filter(Utilisateur.nom == utilisateur_actuel).first()
    
    if utilisateur.est_staff: # type: ignore
        commandes=session.query(Commande).all()
        
        return jsonable_encoder(commandes)  # Encode les données en JSON pour la réponse
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Vous n'êtes pas Super-Utilisateur. Vous n'avez pas les permissions pour accéder à cette ressource")

@order_router.get("/commandes/{id_commande}")
async def liste_commande_par_id(id_commande: int, Authorize: AuthJWT = Depends()):
    #Protéger la route avec AuthJWT
    """
        ## Route pour lister une commande de pizza
        Lister une commande par son identifiant (id_commande).
        Ceci est accessible uniquement aux Super-Utilisateurs (staff).
        
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    
    utilisateur = Authorize.get_jwt_subject()
    
    utilisateur_actuel = session.query(Utilisateur).filter(Utilisateur.nom == utilisateur).first()
    
    if utilisateur_actuel.est_staff: # type: ignore
        commande = session.query(Commande).filter(Commande.id == id_commande).first()
        
        return jsonable_encoder(commande)  # Encode les données en JSON pour la réponse
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Vous n'êtes pas Super-Utilisateur. Vous n'êtes pas autorisé à effectuer cette requête.")

@order_router.get("/utilisateur/commandes")
async def liste_commandes_utilisateur(Authorize: AuthJWT = Depends()):
    # Protéger la route avec AuthJWT
    """
        ## Route pour lister les commandes d'un utilisateur
        Lister toutes les commandes d'un utilisateur connecté.
        Ceci est accessible à tous les utilisateurs authentifiés.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    
    utilisateur = Authorize.get_jwt_subject()
    
    utilisateur_actuel = session.query(Utilisateur).filter(Utilisateur.nom == utilisateur).first()
    
    return jsonable_encoder(utilisateur_actuel.commandes)  # type: ignore # Encode les données en JSON pour la réponse

@order_router.get("/utilisateur/commandes/{id_commande}")
async def liste_commande_utilisateur_par_id(id_commande: int, Authorize: AuthJWT = Depends()):
    # Protéger la route avec AuthJWT
    """
        ## Route pour lister une commande d'un utilisateur par son identifiant (id_commande)
        Lister une commande d'un utilisateur connecté par son identifiant (id_commande).
        Ceci est accessible à tous les utilisateurs authentifiés.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    
    subject = Authorize.get_jwt_subject()
    
    utilisateur_actuel = session.query(Utilisateur).filter(Utilisateur.nom == subject).first()
    
    commandes = utilisateur_actuel.commandes  # type: ignore
    
    for c in commandes:
        if c.id == id_commande:
            return jsonable_encoder(c)  # Encode les données en JSON pour la réponse
    
    # Si aucune commande n'est trouvée pour l'utilisateur avec l'ID donné
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Commande non trouvée pour cet Id (utilisateur).")

@order_router.put("/commande/update/{id_commande}/", status_code=status.HTTP_200_OK)
async def update_commande(id_commande: int, commande: CommandeModel, Authorize: AuthJWT = Depends()):
    # Protéger la route avec AuthJWT
    """
        ## Route pour mettre à jour une commande de pizza
        Mettre à jour une commande de pizza existante.
        Informations nécessaires :
    - **quantite**: int - Nouvelle quantité de pizzas
    - **taille_pizza**: str - Nouvelle taille de la pizza (PETITE, MOYENNE, GRANDE, FAMILIALE)
    """ 
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")  
    
    commande_a_update = session.query(Commande).filter(Commande.id == id_commande).first()
    
    commande_a_update.quantite = commande.quantite
    commande_a_update.taille_pizza = commande.taille_pizza
    
    session.commit()
    
    reponse = {
            "id": commande_a_update.id,
            "quantite": commande_a_update.quantite,
            "taille_pizza": commande_a_update.taille_pizza, # type: ignore
            "statut_commande": commande_a_update.statut_commande # type: ignore
        } 
    
    return jsonable_encoder(reponse)  # Encode les données en JSON pour la réponse

@order_router.patch("/commande/statut/{id_commande}/", status_code=status.HTTP_200_OK)
async def update_statut_commande(id_commande: int, commande: CommandeStatutModel, Authorize: AuthJWT = Depends()):
    # Protéger la route avec AuthJWT
    """
        ## Route pour mettre à jour le statut d'une commande de pizza
        Mettre à jour le statut d'une commande de pizza existante.
        Informations nécessaires :
    - **statut_commande**: str - Nouveau statut de la commande (EN_ATTENTE, EN_LIVRAISON, LIVREE)
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")  
    
    nom = Authorize.get_jwt_subject()
    
    utilisateur_actuel = session.query(Utilisateur).filter(Utilisateur.nom == nom).first()
    
    if utilisateur_actuel.est_staff:  # type: ignore
        commande_a_update = session.query(Commande).filter(Commande.id == id_commande).first()
        
        if commande_a_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande introuvable")
        
        commande_a_update.statut_commande = commande.statut_commande # type: ignore
        
        session.commit()
        
        reponse = {
            "id": commande_a_update.id,
            "quantite": commande_a_update.quantite,
            "taille_pizza": commande_a_update.taille_pizza,
            "statut_commande": commande_a_update.statut_commande
        }
        
        return jsonable_encoder(reponse)  # Encode les données en JSON pour la réponse
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vous n'êtes pas Super-Utilisateur. Vous n'êtes pas autorisé à effectuer cette requête.")

@order_router.delete("/commande/delete/{id_commande}/", status_code=status.HTTP_204_NO_CONTENT)
async def supprimer_commande(id_commande: int, Authorize: AuthJWT = Depends()):
    # Protéger la route avec AuthJWT
    """
        ## Route pour supprimer une commande de pizza
        Supprimer une commande de pizza existante par son identifiant (id_commande).
        Ceci est accessible uniquement aux Super-Utilisateurs (staff).
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    
    commande_a_supprimer = session.query(Commande).filter(Commande.id == id_commande).first()
    
    if commande_a_supprimer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande introuvable")
    
    session.delete(commande_a_supprimer)
    session.commit()
    
    return commande_a_supprimer  # Retourne un code de statut 204 No Content (aucun contenu) pour indiquer que la suppression a réussi sans retourner de données
    
    