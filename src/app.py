import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import src.handlers as handlers
from src.infra.database import create_database
from src.router.hub_router import router as hub_router
from src.router.user_router import router as user_router

app = FastAPI()

BASE_PATH = "/api"


@app.on_event("startup")
async def startup_event() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     %(message)s - DateTime: %(asctime)s",
    )
    logging.info("Starting database connection")
    await create_database()


@app.get("/")
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/health", status_code=204)
async def health() -> None:
    logging.info("Health check")


handlers.register_handlers(app)
app.include_router(user_router, prefix=f"{BASE_PATH}", tags=["User"])
app.include_router(hub_router, prefix=f"{BASE_PATH}", tags=["Hub"])
