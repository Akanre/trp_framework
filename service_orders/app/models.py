from sqlalchemy import Column, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)  # UUID пользователя
    items = Column(JSON, nullable=False)  # Список товаров: [{"name": "", "quantity": 1, "price": 0.0}]
    status = Column(String, default="created")  # created, in_progress, completed, cancelled
    total_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status}, total={self.total_amount})>"