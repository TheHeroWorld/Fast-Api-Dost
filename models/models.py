from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship

# API
class Order(BaseModel):
    name: str
    phone: int
    adress: str
    product: dict[str,int]
    description: str 
    price: float
    
class Review(BaseModel):
    text: str
    rate: int
    orders_id: int



# БАЗА ДАННЫХ

Base = declarative_base()



class Orders(Base):
    __tablename__ = "Orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    adress: Mapped[str] = mapped_column(String(255))
    product: Mapped[str] = mapped_column(String(255))
    price: Mapped[float]
    status: Mapped[str]= mapped_column(String(255),default="Новый заказ")


class Product(Base):
    __tablename__ = "products"
    uuid: Mapped[int] = mapped_column(Integer, unique=True,  primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float]



class Reviews(Base):
    __tablename__ = "Reviews"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    rate: Mapped[int] = mapped_column(Integer, CheckConstraint("rate >= 0 AND rate <= 5"))
    orders_id: Mapped[int] = mapped_column(Integer, ForeignKey("Orders.id"))
    order: Mapped["Orders"] = relationship("Orders", back_populates="reviews")
