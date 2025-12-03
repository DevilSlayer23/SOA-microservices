from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, sku={self.sku}, name={self.name}, price={self.price}, stock={self.stock})>"