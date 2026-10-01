from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routes import router
from app.utils import STATIC_DIR


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "AI Comic Story Creator using "
        "Gemini and Diffusers"
    ),
)


# Static files
app.mount(
    "/static",
    StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static",
)


# Application routes
app.include_router(router)


@app.get("/health")
def health():
    """
    Health check endpoint.
    """

    return {
        "status": "ok",
        "app": settings.app_name,
        "demo_mode": settings.demo_mode,
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
        "local_diffusion_enabled": (
            settings.enable_local_diffusion
        ),
    }