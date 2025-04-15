from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from app.database import engine
from app.models import Product, Order, OrderItem
from datetime import datetime
import uuid

# Import the cart to access the items
from app.routers.cart import cart, clear_cart

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/checkout")
def checkout_page(request: Request):
    # Calculate the total for display in the checkout page
    total = 0
    with Session(engine) as session:
        for pid, qty in cart.items():
            product = session.get(Product, pid)
            if product:
                total += product.price * qty
    
    return templates.TemplateResponse("checkout.html", {"request": request, "total": total})

@router.post("/checkout")
def process_checkout(
    email: str = Form(...), first_name: str = Form(...), last_name: str = Form(...),
    address: str = Form(...), city: str = Form(...), postal_code: str = Form(...), phone: str = Form(...)
):
    # Create an order in the database
    with Session(engine) as session:
        # Calculate the total
        total = 0
        for pid, qty in cart.items():
            product = session.get(Product, pid)
            if product:
                total += product.price * qty
        
        # Create order
        order = Order(
            order_number=str(uuid.uuid4())[:8],
            email=email,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            postal_code=postal_code,
            phone=phone,
            total=total,
            status="pending"
        )
        session.add(order)
        session.commit()
        session.refresh(order)
        
        # Create order items
        for pid, qty in cart.items():
            product = session.get(Product, pid)
            if product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=qty,
                    price=product.price
                )
                session.add(order_item)
        
        session.commit()
    
    # Clear the cart after successful checkout
    clear_cart()
    
    # Redirect to a thank you page (we'll need to create this)
    return RedirectResponse(url="/order/thank-you", status_code=303)

@router.get("/order/thank-you")
def thank_you_page(request: Request):
    return templates.TemplateResponse("thank_you.html", {"request": request})