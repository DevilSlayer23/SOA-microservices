
from app.core.lifespan import lifespan
from fastapi import FastAPI, HTTPException, status
from app.db.session import async_engine # Assuming this is your AsyncEngine instance
from sqlalchemy import text #r
from fastapi.middleware.cors import CORSMiddleware

import logging
from app.core.config import settings
from app.db.session import async_engine
from .routers import router as user_router;
logger = logging.getLogger(__name__)
# Create tables at startup


# ---------------- main app ----------------
app = FastAPI(title="API", lifespan=lifespan)
app.include_router(router=user_router, prefix='/api/users')


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
async def deep_health_check():
    """Checks the application status and database connection health."""
    try:
        # Attempt a quick, lightweight database query
        async with async_engine.begin() as conn:
            # Running SELECT 1 is the standard way to check connection health
            await conn.execute(text("SELECT 1"))
        
        return {"status": "OK", "database": "connected"}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        # If the DB connection fails, return a 503 Service Unavailable
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Database connection failed"
        )

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




