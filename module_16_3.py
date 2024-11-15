from fastapi import FastAPI, Path
import uvicorn
from typing import Annotated
from loguru import logger

app = FastAPI()

logger.add("info.log",format="{time} {level} {message}",level="INFO",rotation="1 month",compression="zip")

users = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users")# функция возвращает словарь, хранящийся в переменной users
async def get_users() -> dict:
    logger.info(users)# записываем в лог словарь из переменной users
    return users

@app.post("/user/{username}/{age}")# функция добавляет пользователя, присваивая ему id (инкремент 1). Параметры добавляемого пользователя ограничены
async def insert_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                     age: int=Path(ge=18, le=120, description='Enter age', example=24)) -> dict:
    max_key = str(int(max(users.keys()))+1)# увеличиваем максимальный user_id на 1
    users[max_key] = f'Имя: {username}, возраст: {age}'# добавление элемента
    logger.info(users) # проверяем в логе, что изменилось в словаре
    return f"User {max_key} is registered"

@app.put("/user/{user_id}/{username}/{age}")# функция изменяет значение элемента по ключу user_id
async def change_user(user_id: Annotated[str, Path(min_value='1', max_value='100', description='Enter user_id', example='50')],
                     username: str=Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser'),
                      age: int=Path(ge=18, le=120, description='Enter age', example=24)) -> str:
    users[user_id] = f'Имя: {username}, возраст: {age}'# присваиваем ключу user_id новое значение
    logger.info(users)# записываем изменения в лог
    return f'The user {user_id} is updated'

@app.delete("/user/{user_id}")# функция удаляет элемент с ключом user_id
async def delete_user(user_id: str=Path(min_value='1', max_value='100', description='Enter user_id', example='50')) -> str:
    del users[user_id]# удаление элемента по ключу user_id
    logger.info(users)# пишем изменившийся словарь в лог
    return f'User {user_id} has been deleted'
