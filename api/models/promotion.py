from decimal import Decimal

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    discount_percent = Column(DECIMAL(5, 2), nullable=False)
    start_date = Column(DATETIME, nullable=False)
    end_date = Column(DATETIME, nullable=False)
