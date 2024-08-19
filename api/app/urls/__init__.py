from fastapi import APIRouter
from .auth import router as auth_urls
from .comments import router as comments_urls
from .likes import router as likes_urls
from .poems import router as poems_urls

router = APIRouter()

router.include_router(auth_urls)
router.include_router(comments_urls)
router.include_router(likes_urls)
router.include_router(poems_urls)
