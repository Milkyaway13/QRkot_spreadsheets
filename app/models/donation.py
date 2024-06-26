from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base

from .base_model import InvestModelBase


class Donation(Base, InvestModelBase):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
