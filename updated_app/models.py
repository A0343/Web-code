from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    image_url: str
    category: str
    availability: bool = True
    size: str

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_number: str = Field(unique=True)
    email: str
    first_name: str
    last_name: str
    address: str
    city: str
    postal_code: str
    phone: str
    total: float
    status: str  # pending, paid, shipped, delivered
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    items: List["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    price: float
    
    order: Order = Relationship(back_populates="items")
    product: Product = Relationship()