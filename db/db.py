from sqlalchemy import create_engine, Column, Integer, String, select, insert, update, delete
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Base, Orders, Reviews,Product
from dotenv import load_dotenv
import asyncio


load_dotenv()

SQL_SEVER = os.getenv("SQL_SEVER")

engine = create_async_engine(SQL_SEVER, echo=False)
async_session = async_sessionmaker(engine)

async def install_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  #Создаем базу данных и првоеряем есть ли она вообще


async def get_price(product_id):
    products = list(product_id.keys()) # Достам из словаря клчюи
    num = list(product_id.values()) # Достмаем значения
    async with async_session() as session:
        total_price = 0
        for prod,quantity in zip(products, num):  #Перебираем данные для дальнейшего подсчета итоговой суммы
            stmt = select(Product.price).filter(Product.name == prod)
            result = await session.execute(stmt)
            price = result.scalars().first()
            total_price += price * quantity  # Считаем ИТОГ
    return total_price

async def order(order): # Принимаем данные по заказу и записываем в базу данных
    async with async_session() as session:
        product = list(order.product.items()) # Достаем из из словаря данные по продуктам и превращаем его в лист
        total_price = await get_price(order.product) # Вызываем метод который считает цену заказа
        products =", ".join(f"{product}: {val}" for product, val in product) # Обьединяем все продукты и их колеичество в один лист
        stmt = (
            insert(Orders).values(name=order.name,adress =order.adress, product = products, price = total_price)
        )# Отправялем данные в базу данных
        result = await session.execute(stmt)
        order_id = result.inserted_primary_key[0]
        await session.commit()
        return order_id


async def get_order(order_id): 
    async with async_session() as session:
        stmt = select(Orders).where(Orders.id == order_id) # Берем заказ по его id
        result = await session.execute(stmt)
        orders = result.scalars().first()
        return orders
    

 
async def get_all_order():
    async with async_session() as session:
        stmt = select(Orders) # Достаем из базы данных всез заказы 
        result = await session.execute(stmt)
        orders = result.scalars().all()
        return orders
    
async def update_status(id, new_status):
    async with async_session() as session:
        stmt = update(Orders).where(Orders.id == id).values(status = new_status) #Изменяем статус, зависимо от Id Заказа
        await session.execute(stmt)
        await session.commit()
        
        
async def delete_order(id):
    async with async_session() as session:
        stmt = delete(Orders).where(Orders.id == id) #Удаляем заказ, зависимо от Id Заказа
        await session.execute(stmt)
        await session.commit()
        
        
        
async def get_Review(review): # Принимаем данные по заказу и записываем в базу данных
    async with async_session() as session:
        stmt = (
            insert(Reviews).values(text=review.text,rate=review.rate, orders_id=review.orders_id))# Отправялем данные в базу данных
        result = await session.execute(stmt)
        await session.commit()