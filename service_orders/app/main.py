from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Order
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Orders Service", version="1.0.0")

# Настройка базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./orders.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic схемы
class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total_amount: float

class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: List[Dict]
    status: str
    total_amount: float
    created_at: str
    updated_at: str

# Временная заглушка для аутентификации (в реальном приложении будет JWT)
def get_current_user():
    """Заглушка для получения текущего пользователя"""
    return {"user_id": "engineer-user-id", "email": "engineer@company.com"}

# API endpoints
@app.post("/v1/orders", response_model=dict)
async def create_order(order_data: OrderCreate, db = Depends(get_db)):
    """Создание нового заказа"""
    try:
        # В реальном приложении user_id будет из JWT токена
        current_user = get_current_user()
        user_id = current_user["user_id"]
        
        # Валидация items
        if not order_data.items:
            raise HTTPException(status_code=400, detail="Order must contain at least one item")
        
        for item in order_data.items:
            if item.quantity <= 0:
                raise HTTPException(status_code=400, detail="Item quantity must be positive")
            if item.price < 0:
                raise HTTPException(status_code=400, detail="Item price cannot be negative")
        
        # Создание заказа
        db_order = Order(
            user_id=user_id,
            items=[item.dict() for item in order_data.items],
            total_amount=order_data.total_amount,
            status="created"
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        logger.info(f"Order created: {db_order.id} for user: {user_id}")
        
        return {
            "success": True,
            "data": {
                "id": db_order.id,
                "user_id": db_order.user_id,
                "items": db_order.items,
                "status": db_order.status,
                "total_amount": db_order.total_amount,
                "created_at": db_order.created_at.isoformat(),
                "updated_at": db_order.updated_at.isoformat()
            }
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/v1/orders", response_model=dict)
async def get_orders(db = Depends(get_db)):
    """Получение списка заказов текущего пользователя"""
    try:
        # В реальном приложении user_id будет из JWT токена
        current_user = get_current_user()
        user_id = current_user["user_id"]
        
        orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": order.id,
                    "user_id": order.user_id,
                    "items": order.items,
                    "status": order.status,
                    "total_amount": order.total_amount,
                    "created_at": order.created_at.isoformat(),
                    "updated_at": order.updated_at.isoformat()
                }
                for order in orders
            ]
        }
        
    except Exception as e:
        logger.error(f"Error fetching orders: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/v1/orders/{order_id}", response_model=dict)
async def get_order(order_id: str, db = Depends(get_db)):
    """Получение заказа по ID"""
    try:
        current_user = get_current_user()
        user_id = current_user["user_id"]
        
        order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return {
            "success": True,
            "data": {
                "id": order.id,
                "user_id": order.user_id,
                "items": order.items,
                "status": order.status,
                "total_amount": order.total_amount,
                "created_at": order.created_at.isoformat(),
                "updated_at": order.updated_at.isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching order {order_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def root():
    return {"message": "Orders Service is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "orders"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)