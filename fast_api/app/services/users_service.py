# app/services/users_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 
from app.models.users_model import User

from app.core.security import hash_password


class UsersService:

    # Async versions of the service methods

    # Get list of users
    @staticmethod
    async def list(db: AsyncSession):
        result = await db.execute(select(User))
        return result.scalars().all()
    
    # Create a new user
    @staticmethod
    async def create(db: AsyncSession, data : dict):
        print("PASSWORD RAW:", data["password"], type(data["password"]))

        password = data.get("password")
        if not password:
            raise ValueError("Password is required.")

        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password too long. Max 72 bytes.")

        hashed_password = hash_password(password)
        user = User(
            email=data.get('email'),
            password=hashed_password,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_active=data.get('is_active', True),
            is_superuser=data.get('is_superuser', False)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    # Get a user by ID
    @staticmethod
    async def get(db: AsyncSession, user_id: int):
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()
    
    # Delete a user by ID
    @staticmethod
    async def delete(db: AsyncSession, user_id: int):
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if user:
            await db.delete(user)
            await db.commit()
            return user
        return None
    
    # Get a user by email
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    

    
    # Synchronous versions of the service methods (if needed)

    # @staticmethod
    # def list(db: Session):
    #     return db.query(User).all()


    # @staticmethod
    # def create(db: Session, data):
    #     user = User(**data)
    #     db.add(user)
    #     db.commit()
    #     db.refresh(user)
    #     return user


    # @staticmethod
    # def get(db: Session, user_id: int):
    #     return db.query(User).filter(User.id == user_id).first()


    # @staticmethod
    # def delete(db: Session, user_id: int):
    #     user = db.query(User).filter(User.id == user_id).first()
    #     if user:
    #         db.delete(user)
    #         db.commit()
    #         return user
    #     return None