from fastapi import APIRouter, Request, Form, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from app.database import engine
from app.models import Product
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Simple in-memory cart - in a real app we'd use a database or session
cart = {}

@router.post("/cart/add")
def add_to_cart(product_id: int = Form(...), response: Response = None):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product or not product.availability:
            raise HTTPException(status_code=404, detail="Product not found or out of stock")
    
    cart.setdefault(product_id, 0)
    cart[product_id] += 1
    
    # Redirect back to the referring page
    return RedirectResponse(url="/cart", status_code=303)

@router.post("/cart/update")
def update_cart(product_id: int = Form(...), quantity: int = Form(...)):
    if product_id in cart:
        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            del cart[product_id]
        else:
            cart[product_id] = quantity
    
    return RedirectResponse(url="/cart", status_code=303)

@router.post("/cart/remove")
def remove_from_cart(product_id: int = Form(...)):
    if product_id in cart:
        del cart[product_id]
    
    return RedirectResponse(url="/cart", status_code=303)

@router.get("/cart")
def view_cart(request: Request):
    items = []
    total = 0
    with Session(engine) as session:
        for pid, qty in cart.items():
            product = session.get(Product, pid)
            if product:
                items.append({"product": product, "quantity": qty})
                total += product.price * qty
    
    return templates.TemplateResponse("cart.html", {"request": request, "items": items, "total": total})

@router.post("/cart/clear")
def clear_cart():
    cart.clear()
    return RedirectResponse(url="/cart", status_code=303)