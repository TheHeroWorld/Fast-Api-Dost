from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from db import db

from models.models import Order, Review



app = FastAPI()


@app.post("/orders")
async def new_orders(order: Order):
    order_id = await db.order(order)  # Принимаем body и отарвяем их в БД
    return {"oder_id":order_id}


@app.get("/orders/{id}")
async def get_oders(id:int):
    order = await db.get_order(id)  # Получаем ID и отправялем запрос в БД
    data = {
            "id": order.id,
            "name": order.name,
            "address": order.adress,
            "product": order.product,
            "price": order.price,
            "status": order.status,
        }
    return data

@app.get("/orders")
async def get_oders():
    orders = await db.get_all_order()  # Просто берем все возможнеы заказы из базы данных
    back = []
    for order in orders:
        data = {
                "id": order.id,
                "name": order.name,
                "address": order.adress,
                "product": order.product,
                "price": order.price,
                "status": order.status,
                }
        back.append(data)
    return back


@app.put("/orders/{id}")
async def get_oders(id:int,status:str):
    order = await db.get_order(id)
    list_status= ["Новый заказ", "Готовится", "Готов", "Заказ закрыт"]
    if status not in list_status or order is None:
        raise HTTPException(
            status_code=403,
            detail="invalid value",
        )
    if order:
        await db.update_status(id, status)
        return f"Новый статус {status}"
    
    
@app.delete("/orders/{id}")
async def get_oders(id:int):
    order = await db.get_order(id)
    if order is None:
        raise HTTPException(
            status_code=403,
            detail="invalid value",
        )
    request = await db.delete_order(id)
    return request


@app.post("/reviews")
async def new_orders(review: Review):
    data = await db.get_Review(review)  # Принимаем body и отарвяем их в БД
    return {"Review":data}