import fastapi
import uvicorn

from src.api.endpoints import router as api_endpoint_router
from src.config.events import execute_backend_server_event_handler, terminate_backend_server_event_handler
from src.config.manager import settings
from src.initial.index import on_start
from fastapi.staticfiles import StaticFiles


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI(**settings.set_backend_app_attributes)  # type: ignore

    app.add_event_handler(
        "startup",
        execute_backend_server_event_handler(backend_app=app),
    )
    app.add_event_handler(
        "shutdown",
        terminate_backend_server_event_handler(backend_app=app),
    )

    on_start(app)

    app.include_router(router=api_endpoint_router, prefix=settings.api_prefix)

    app.mount("/", StaticFiles(directory="public", html=True), name="public")

    return app


backend_app: fastapi.FastAPI = initialize_backend_application()


# if __name__ == "__main__":
#     uvicorn.run(
#         app="main:backend_app",
#         host=settings.server_host,
#         port=settings.server_port,
#         reload=settings.debug,
#         workers=settings.server_workers,
#         log_level=settings.logging_level,
#     )


def start():
    uvicorn.run(
        app="src.main:backend_app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
        workers=settings.server_workers,
        log_level=settings.logging_level,
    )
