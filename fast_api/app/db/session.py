

from typing import Any, AsyncGenerator
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker





@as_declarative()
class Base:
    id: Any
    __name__: str

    #to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    


DATABASE_URL = settings.DB_URL

# Print the type of DATABASE_URL
print(f"Type of DATABASE_URL: {type(DATABASE_URL)}")
# For logging purposes
print(f"Database URL: {DATABASE_URL}")
    
# Create the SQLAlchemy  async engine and sessionmaker
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True, )

# Create a session factory

AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


# Create a dependency to get the async database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session