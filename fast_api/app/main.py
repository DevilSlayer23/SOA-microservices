from datetime import datetime, timezone
from contextlib import asynccontextmanager
from app.core.lifespan import lifespan
from app.db.session import Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Engine
from app.routers import products as products_router
from app.routers import users as users_router
import uvicorn
import logging
from app.core.config import settings
from app.db.session import async_engine


logger = logging.getLogger(__name__)
# Create tables at startup


# ---------------- main app ----------------
app = FastAPI(title="API", lifespan=lifespan)
app.include_router(router=products_router.router, prefix='/products')
app.include_router(router=users_router.router, prefix='/users')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


# ---------------- main app ----------------

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Gateway"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.get("/info")
def app_info():
    return {
        "project_name": settings.PROJECT_NAME,
        "project_version": settings.PROJECT_VERSION,
        "database": {
            "postgres_user": settings.POSTGRES_USER,
            "postgres_db": settings.POSTGRES_DB,
            "postgres_host": settings.POSTGRES_HOST,
            "postgres_port": settings.POSTGRES_PORT,
        },
        "redis": {
            "redis_host": settings.REDIS_HOST,
            "redis_port": settings.REDIS_PORT,
            "redis_db": settings.REDIS_DB,
        }
    }   




