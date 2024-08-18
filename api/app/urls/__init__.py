from fastapi import APIRouter
from .auth import router as auth_urls
from .poems import router as poems_urls

router = APIRouter()

router.include_router(auth_urls)
router.include_router(poems_urls)
