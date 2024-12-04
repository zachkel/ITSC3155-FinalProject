from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Resource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    unit = Column(String, nullable=False)
