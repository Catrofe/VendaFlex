import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import src.handlers as handlers


app = FastAPI()

BASE_PATH = "/api"


@app.on_event("startup")
async def startup_event() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(message)s - DateTime: %(asctime)s")
    logging.info("Starting up...")


@app.get("/")
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")

@app.get("/health", status_code=204)
async def health() -> None:
    logging.info("Health check")

handlers.register_handlers(app)