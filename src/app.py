import logging
import logging.config
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI()

BASE_PATH = "/api"


@app.on_event("startup")
async def startup_event(url: Optional[str] = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(message)s - DateTime: %(asctime)s - ")
    logging.info("Starting up...")


@app.get("/")
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")
