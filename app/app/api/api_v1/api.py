####################################################################################################

from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils, donations, stripe_webhook

####################################################################################################

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(donations.router, prefix="/donations", tags=["donations"])
api_router.include_router(stripe_webhook.router, prefix="/stripe_webhook", tags=["stripe_webhook"])