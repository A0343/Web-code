from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.database import engine
from app.models import Product
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", include_in_schema=False)
def home(request: Request):
    with Session(engine) as session:
        # Get featured products (limited to 4)
        products = session.exec(select(Product).limit(4)).all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@router.get("/products")
def product_list(
    request: Request,
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    sort: Optional[str] = Query(None)
):
    with Session(engine) as session:
        query = select(Product)
        
        # Apply filters if provided
        if category:
            query = query.where(Product.category == category)
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)
        
        # Apply sorting if provided
        if sort == "price_asc":
            query = query.order_by(Product.price)
        elif sort == "price_desc":
            query = query.order_by(Product.price.desc())
        elif sort == "name_asc":
            query = query.order_by(Product.name)
        elif sort == "name_desc":
            query = query.order_by(Product.name.desc())
        
        products = session.exec(query).all()
    
    return templates.TemplateResponse(
        "products.html", 
        {
            "request": request, 
            "products": products,
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "sort": sort
        }
    )

@router.get("/products/{product_id}")
def product_detail(request: Request, product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
    
    # Get related products (same category)
    with Session(engine) as session:
        related_query = select(Product).where(
            Product.category == product.category,
            Product.id != product.id
        ).limit(4)
        related_products = session.exec(related_query).all()
    
    return templates.TemplateResponse(
        "product_detail.html", 
        {
            "request": request, 
            "product": product,
            "related_products": related_products
        }
    )