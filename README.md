## API DE LIVRAISON DE PIZZAS

Cette API REST sert un service de livraison de pizzas, conçue avec **FastAPI**, **SQLAlchemy** et **PostgreSQL**.

---

## Routes à implémenter

| Méthode   | Route                                  | Fonctionnalité                                | Accès            |
|-----------|----------------------------------------|-----------------------------------------------|------------------|
| **POST**  | `/auth/inscription/`                        | Enregistrer un nouvel utilisateur             | Tous les utilisateurs |
| **POST**  | `/auth/connexion/`                         | Authentifier un utilisateur                   | Tous les utilisateurs |
| **POST**  | `/commandes/commande/`                       | Passer une commande                           | Tous les utilisateurs |
| **PUT**   | `/commandes/commande/update/{id_commande}/`     | Mettre à jour une commande                    | Tous les utilisateurs |
| **PUT**   | `/commandes/commande/status/{id_commande}/`     | Mettre à jour le statut d’une commande        | Super-utilisateur     |
| **DELETE**| `/commandes/commande/delete/{id_commande}/`     | Supprimer une commande                        | Tous les utilisateurs |
| **GET**   | `/commandes/utilisateur/commande/`                 | Récupérer toutes les commandes d’un utilisateur | Tous les utilisateurs |
| **GET**   | `/commandes/commande/`                      | Lister toutes les commandes                    | Super-utilisateur     |
| **GET**   | `/commandes/commande/{id_commande}/`           | Récupérer une commande par son identifiant     | Super-utilisateur     |
| **GET**   | `/commandes/utilisateur/commande/{id_commande}/`       | Récupérer une commande spécifique d’un utilisateur | Tous les utilisateurs |
| **GET**   | `/docs/`                               | Afficher la documentation interactive (Swagger) | Tous les utilisateurs |

---

## Comment exécuter le projet

1. **Installer PostgreSQL**  
2. **Installer Python 3.8+**  
3. **Configurer la base de données**  
   Dans `database.py`, définir l’URL de connexion :  
   ```python
   from sqlalchemy import create_engine

   engine = create_engine(
       'postgresql://postgres:<username>:<password>@localhost/<db_name>',
       echo=True
   )

La toute première étape, avant même d’écrire une ligne de code métier, consiste à préparer et valider la connexion à la base de données et à définir les entités (modèles SQLAlchemy). 

## Description des fichiers Python:

# 1. database.py 
database.py → On y crée l’engine SQLAlchemy (avec votre URI PostgreSQL) et la SessionLocal.

# 2. models.py
models.py → On y définit les classes–tables SQLAlchemy (Utilisateur, Commande, etc.).

# 3. init_db.py
init_db.py → On importe l’engine et les modèles pour lancer Base.metadata.create_all(engine) et ainsi créer physiquement les tables dans PostgreSQL.

Une fois ce socle « base de données » posé, on peut passer aux :

# 4. schemas.py
schemas.py → Modèles Pydantic pour valider / documenter les payloads JSON.

# 5. auth_routes.py 
auth_routes.py → Endpoint, s’appuyant sur les SessionLocal, models et schemas.

# 6. order_routes.py 
order_routes.py → Endpoints, s’appuyant sur les SessionLocal, models et schemas.

# 7. main.py
main.py → Où l’on assemble tout : on importe les routers, on configure FastAPI, la sécurité, la doc interactive.

