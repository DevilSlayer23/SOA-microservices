from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.products_service import ProductsService
from app.schemas.products_schema import ProductCreate, ProductRead
from typing import List


router = APIRouter(tags=["products"])


@router.get("/", response_model=List[ProductRead])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await ProductsService.list(db)


@router.post("/", response_model=ProductRead)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await ProductsService.create(db, product.dict())


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductsService.get(db, product_id)


@router.delete("/{product_id}", response_model=ProductRead)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductsService.delete(db, product_id)


# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.db.session import AsyncSessionLocal, get_db
# from app.models.product_model import Product
# from app.services.products_service import ProductsService


# router = APIRouter(prefix="/products", tags=["products"])

# # Create async versions of the endpoints
# @router.get("/", response_model=list[Product])
# async def list_products(db: AsyncSession = Depends(get_db)):
#     return await ProductsService.list(db)

# @router.post("/", response_model=Product)
# async def create_product(data: Product, db: AsyncSession = Depends(get_db)):
#     return await ProductsService.create(db, data.to_dict())

# @router.get("/{product_id}", response_model=Product)
# async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
#     return await ProductsService.get(db, product_id)

# @router.delete("/{product_id}")
# async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
#     return await ProductsService.delete(db, product_id) 


# Synchronous versions of the endpoints (if needed)

# def get_db():
#     db = AsyncSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.get("/")
# def list_products(db: Session = Depends(get_db)):
#     return ProductsService.list(db)
    

# @router.post("/")
# def create_product(data: dict, db: Session = Depends(get_db)):
#     return ProductsService.create(db, data)

# @router.get("/{product_id}")
# def get_product(product_id: int, db: Session = Depends(get_db)):
#     return ProductsService.get(db, product_id)  

# @router.delete("/{product_id}")
# def delete_product(product_id: int, db: Session = Depends(get_db)):
#     return ProductsService.delete(db, product_id)