from fastapi import FastAPI

from api.lifespan import lifespan
from api.routers.health import router as health_router
from api.routers.admin.access import router as access_router
from api.routers.admin.clients import router as clients_router
from api.routers.user.cabinet import router as cabinet_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Hosting API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(health_router, prefix="/api/v1")
    app.include_router(access_router, prefix="/api/v1")
    app.include_router(clients_router, prefix="/api/v1")
    app.include_router(cabinet_router, prefix="/api/v1")

    return app

app = create_app()

