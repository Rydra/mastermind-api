# type: ignore

import django

django.setup()  # noqa

from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from apps.mastermind.infrastructure.api.entrypoints import router as game_router
from composite_root.bootstrapper import bootstrap

description = """
Mastermind REST API
"""

app = FastAPI(
    root_path="/",
    title="Mastermind API",
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


@app.get("/hc")
def get_status():
    return JSONResponse(content={"time": str(datetime.utcnow())})
