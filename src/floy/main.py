import os
import subprocess
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from src.floy.routers.series import router as series_router


def get_app() -> FastAPI:
    app = FastAPI(
        title="Series API",
        description="API for receiving PACS series",
        name="Series API",
    )

    app.include_router(series_router)

    return app


application = get_app()


@application.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@application.on_event("startup")
async def startup_event() -> None:
    # HACK solution to run alembic migrations on startup! REMOVE THIS FOR PRODUCTION
    # Running alembic migrations here to make it easier to run the app for
    # demoing purposes.  REMOVE THIS FOR PRODUCTION
    current_directory = os.getcwd()
    alembic_directory = Path(__file__).parent.parent.parent
    os.chdir(alembic_directory)
    subprocess.run(["alembic", "upgrade", "head"])
    os.chdir(current_directory)


if __name__ == "__main__":
    subprocess.run(["ls"])
    uvicorn.run(
        "src.floy.main:application",
        reload=True,
    )
