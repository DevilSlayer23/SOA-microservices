from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product_model import Product



class ProductsService:

    # Async versions of the service methods

    # Get list of products
    @staticmethod
    async def list(db: AsyncSession):
        result = await db.execute(select(Product))
        return result.scalars().all()
    
    # Create a new product
    @staticmethod
    async def create(db: AsyncSession, data):
        product = Product(**data)
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product
    
    # Get a product by ID
    @staticmethod
    async def get(db: AsyncSession, product_id: int):
        result = await db.execute(select(Product).filter(Product.id == product_id))
        return result.scalars().first()
    
    # Delete a product by ID
    @staticmethod
    async def delete(db: AsyncSession, product_id: int):
        result = await db.execute(select(Product).filter(Product.id == product_id))
        product = result.scalars().first()
        if product:
            await db.delete(product)
            await db.commit()
            return product
        return None
    
    # Synchronous versions of the service methods (if needed)

    # @staticmethod
    # def list(db: Session):
    #     return db.query(Product).all()


    # @staticmethod
    # def create(db: Session, data):
    #     product = Product(**data)
    #     db.add(product)
    #     db.commit()
    #     db.refresh(product)
    #     return product


    # @staticmethod
    # def get(db: Session, product_id: int):
    #     return db.query(Product).filter(Product.id == product_id).first()


    # @staticmethod
    # def delete(db: Session, product_id: int):
    #     product = db.query(Product).filter(Product.id == product_id).first()
    #     if product:
    #         db.delete(product)
    #         db.commit()
    #         return product
    #     return None