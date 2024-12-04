from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    card_info = Column(String, nullable=False)
    transaction_status = Column(String, nullable=False)
    payment_type = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)

    customer = relationship('Customer', back_populates='payments')
