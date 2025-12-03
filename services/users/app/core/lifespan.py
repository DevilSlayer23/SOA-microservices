import platform
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import configuration
from app.db.session import async_engine, Base
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler


logger = logging.getLogger(__name__)



# ---------------- lifespan ----------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app_name = app.title
        environment = "production" if configuration.IS_PRODUCTION else "sandbox"
        startup_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
        python_version = platform.python_version()
        app.state.config = configuration
        # If you want auto-generated tables from model
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        # Start Scheduler (example job)
        scheduler = AsyncIOScheduler()
        async def housekeeping():
            logger.info("housekeeping tick")
        scheduler.add_job(housekeeping, "interval", minutes=5)
        scheduler.start()
        app.state.scheduler = scheduler
        # Startup log
        logger.info(
            "\n=========================================\n"
            "          Application Startup            \n"
            "=========================================\n"
            f"App Name        : {app_name}\n"
            f"Environment     : {environment}\n"
            f"Startup Time    : {startup_time}\n"
            f"Python Version  : {python_version}\n"
            "=========================================\n"
        )
        yield
        # Shutdown
        scheduler.shutdown(wait=False)
        shutdown_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
        logger.info(
            "\n=========================================\n"
            "          Application Shutdown           \n"
            "=========================================\n"
            f"Shutdown Time   : {shutdown_time}\n"
            "=========================================\n"
        )
    except Exception as e:
        logger.error(f"Lifespan error: {e}")
        raise e
# ---------------- lifespan ----------------