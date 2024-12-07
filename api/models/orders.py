from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
from .order_details import OrderDetail

class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    tracking_number = Column(String, unique=True, nullable=False)
    order_status = Column(String, nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_type = Column(String, nullable=False)

    customer = relationship('Customer', back_populates='orders')
    items = relationship('OrderDetail', back_populates='order')
