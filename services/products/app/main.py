from datetime import datetime, timezone
from contextlib import asynccontextmanager
import time

from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest
from app.core.lifespan import lifespan
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import FastAPI, HTTPException, Request,status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Engine, text
from app.routers import products as products_router
import uvicorn
import logging
from app.core.config import settings
from app.db.session import async_engine


logger = logging.getLogger(__name__)
# Create tables at startup


# ---------------- main app ----------------
app = FastAPI(title="Orders API", lifespan=lifespan)
app.include_router(router=products_router.router, prefix='/api/products')



# =============================
# METRICS MIDDLEWARE
# =============================

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()

        response = None
        try:
            response = await call_next(request)
        except Exception as exc:
            # Track unhandled errors
            endpoint = request.url.path
            error_counter.labels(
                endpoint=endpoint,
                status_code="500"
            ).inc()
            raise exc

        endpoint = request.url.path

        # Skip internal endpoints
        if endpoint not in ('/favicon.ico', '/metrics'):
            endpoint_clicks.labels(endpoint=endpoint).inc()

            latency = time.time() - start
            endpoint_latency.labels(endpoint=endpoint).observe(latency)

            client_ip = request.client.host
            lat, lon = await get_location(client_ip)
            user_locations.labels(latitude=str(lat), longitude=str(lon)).inc()

        return response
    

## Middlewares

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


# =============================
# PROMETHEUS METRICS
# =============================

endpoint_clicks = Counter(
    'endpoint_clicks',
    'Total clicks per endpoint',
    ['endpoint']
)

endpoint_latency = Histogram(
    'endpoint_latency_seconds',
    'Endpoint response time',
    ['endpoint']
)

user_locations = Counter(
    'unique_user_locations',
    'Unique user locations',
    ['latitude', 'longitude']
)

error_counter = Counter(
    'endpoint_errors',
    'Total errors per endpoint and status code',
    ['endpoint', 'status_code']
)


# =============================
# IP LOCATION LOOKUP
# =============================

async def get_location(ip: str):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f'http://ip-api.com/json/{ip}')
            data = r.json()
            if data.get("status") == "success":
                return [data["lat"], data["lon"]]
    except Exception:
        pass
    return [0.0, 0.0]
    


# =============================
# EXCEPTION HANDLERS
# =============================

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    endpoint = request.url.path
    error_counter.labels(endpoint=endpoint, status_code="500").inc()

    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected error occurred: {str(exc)}"}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    endpoint = request.url.path
    error_counter.labels(endpoint=endpoint, status_code=str(exc.status_code)).inc()

    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


# =============================
# METRICS ENDPOINT
# =============================

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest().decode("utf-8"))

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




