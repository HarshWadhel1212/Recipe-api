"""Starting point of the application."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (makes sure tables are registered)
from app.database import Base, engine
from app.routers import recipes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the server starts: create tables if they do not exist.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Recipe Management API",
    description="A simple REST API to manage recipes, built with FastAPI and PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(recipes.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
