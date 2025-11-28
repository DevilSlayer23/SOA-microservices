from http.client import HTTPException
from passlib.hash import bcrypt
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.users_service import UsersService
from app.schemas.users_schema import LoginRequest, UserCreate, UserRead
from typing import List
from app.core.auth import create_access_token
from app.models.users_model import User


router = APIRouter(tags=["users"])


@router.get("/", response_model=List[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await UsersService.list(db)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UsersService.get(db, user_id)


@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UsersService.delete(db, user_id)

# Endpoints for user related operations
@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    exists = await UsersService.get_by_email(db, user.email)
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    created = await UsersService.create(db, user.model_dump())
    return created

@router.post("/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await UsersService.get_by_email(db, payload.email)
    if not user or not bcrypt.verify(payload.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)}, expires_delta=60)
    return {"access_token": token, "token_type": "bearer"}




# Synchronous versions of the endpoints (if needed)

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.db.session import get_db
# from app.models.users_model import User
# from app.services.users_service import UsersService



# router = APIRouter(prefix="/users", tags=["users"])
# # Create async versions of the endpoints
# @router.get("/", response_model=list[User])
# async def list_users(db: Session = Depends(get_db)):
#     return await UsersService.list(db)

# @router.post("/", response_model=User)
# async def create_user(data: User, db: Session = Depends(get_db)):
#     return await UsersService.create(db, data.to_dict())

# @router.get("/{user_id}", response_model=User)
# async def get_user(user_id: int, db: Session = Depends(get_db)):
#     return await UsersService.get(db, user_id)

# @router.delete("/{user_id}")
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     return await UsersService.delete(db, user_id)

# Synchronous versions of the endpoints (if needed)

# def get_db():
#     db = AsyncSessionLocal
#     try:
#         yield db
#     finally:
#         db.close()


# @router.get("/")
# def list_users(db: Session = Depends(get_db)):
#     return UsersService.list(db)


# @router.post("/")
# def create_user(data: dict, db: Session = Depends(get_db)):
#     return UsersService.create(db, data)


# @router.get("/{user_id}")
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     return UsersService.get(db, user_id)


# @router.delete("/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     return UsersService.delete(db, user_id)