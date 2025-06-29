from fastapi import APIRouter
 
# ----------------------------------------------------------------
# Routeur dédié aux opérations sur les commandes (/commandes)
# ----------------------------------------------------------------
order_router = APIRouter(
    prefix="/commandes",
    tags=["commandes"]
)
@order_router.get("/")
async def hello():
    return {"message": "Hello de *Commandes router!*"}