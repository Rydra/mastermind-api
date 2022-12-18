# type: ignore

import django

django.setup()  # noqa

from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from apps.mastermind.fastapi.entrypoints import router as game_router
from composite_root.bootstrapper import bootstrap

description = """
MasterMind API give you the basic endpoint for creating this game
## Overview
You will be able to:
* **Create a new game**
* **Adding guess and getting the response**
* **Getting the current state of a game**
"""

app = FastAPI(
    root_path="/",
    title="MasterMind API",
    description=description,
    version="0.0.1",
    docs_url="/openapi",
    redoc_url="/redoc",
    contact={
        "name": "David Jiménez",
        "email": "davigetto@gmail.com@gmail.com",
    },
)
app.include_router(game_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    bootstrap()


@app.get("/server-status")
def get_status():
    return JSONResponse(content={"time": str(datetime.utcnow())})
