from fastapi import APIRouter

from api.endpoints.administrator import router as admin_router
from api.endpoints.auth import router as auth_router
from api.endpoints.user import router as user_router
from api.endpoints.webhooks import router as webhook_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authorization"])
router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(
    admin_router, prefix="/administrator", tags=["Administrator"])
router.include_router(webhook_router, prefix="/webhooks", tags=["Webhooks"])
