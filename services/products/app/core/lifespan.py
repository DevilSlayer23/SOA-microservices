import platform
import logging
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings  # use the cleaned-up Settings model
from app.db.session import async_engine, Base

logger = logging.getLogger(__name__)

def format_time(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    try:
        # Store config
        app.state.settings = settings
        environment = "production" if settings.IS_PRODUCTION else "sandbox"

        # Create tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Scheduler job example
        async def housekeeping():
            logger.info("Housekeeping tick")

        scheduler.add_job(housekeeping, "interval", minutes=5)
        scheduler.start()
        app.state.scheduler = scheduler

        # Startup logging
        logger.info(
            "\n=========================================\n"
            "          Application Startup            \n"
            "=========================================\n"
            f"App Name        : {app.title}\n"
            f"Environment     : {environment}\n"
            f"Startup Time    : {format_time(datetime.now())}\n"
            f"Python Version  : {platform.python_version()}\n"
            "=========================================\n"
        )

        yield  # hand control back to FastAPI

    except Exception as e:
        logger.exception("Error during app lifespan")
        raise e

    finally:
        # Shutdown
        if scheduler.running:
            scheduler.shutdown(wait=False)
        logger.info(
            "\n=========================================\n"
            "          Application Shutdown           \n"
            "=========================================\n"
            f"Shutdown Time   : {format_time(datetime.now())}\n"
            "=========================================\n"
        )
