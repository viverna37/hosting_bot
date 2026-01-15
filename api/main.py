from fastapi import FastAPI

from api.lifespan import lifespan
from api.routers.health import router as health_router
from api.routers.admin.auth import router as admin_auth

def create_app() -> FastAPI:
    app = FastAPI(
        title="Hosting API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(health_router, prefix="/api/v1")
    app.include_router(admin_auth, prefix="/api/v1")

    return app

app = create_app()

