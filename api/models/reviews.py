from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    review_text = Column(String)
    score = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)

    customer = relationship('Customer', back_populates='reviews')
