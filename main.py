import asyncio
from db import db
import uvicorn

# Запуск АПИ и Базы данных
if __name__ =="__main__":
    asyncio.run(db.install_db())
    uvicorn.run("app.app:app", reload=True)
    