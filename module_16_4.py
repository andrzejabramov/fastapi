import json
from fastapi import FastAPI, Path, HTTPException
import uvicorn
from typing import Annotated
from fastapi.openapi.utils import status_code_ranges
from loguru import logger
from models import User

app = FastAPI()

logger.add("info_16_4.log",format="{time} {level} {message}",level="INFO",rotation="1 month",compression="zip")

users = []


@app.get("/users")# функция возвращает словарь, хранящийся в переменной users
async def get_users() -> list:
    logger.info(f'GET: {users}')# записываем в лог словарь из переменной users
    return users

@app.post("/users/")# функция добавляет пользователя, присваивая ему id (инкремент 1). Аргументы добавляемого пользователя валидируются
async def insert_user(new_user: User) -> dict:
    new_user = new_user.dict()#преобразуем входящий json в словарь
    if len(users) == 0:# если пользователь не отредактировал или неверно отредактировал поле id в swaggers
        max_id = 1# если список пока пустой
    else:
        max_id = max([el['id'] for el in users]) + 1# если в списке есть элементы, то значение id увеличиваем на 1
    new_user['id'] = max_id #устанавливаем значение id
    users.append(new_user) # добавление элемента
    logger.info(f'POST: {users}') # проверяем в логе, что изменилось в словаре
    return new_user

@app.put("/users")# функция изменяет значение элемента по ключу user_id
async def change_user(update_user: User) -> dict:# функция изменяет данные по пользователю, если он существует
    try:
        update_user = update_user.dict()# преобразуем json в dict
        val_id = update_user['id'] #определяем id изменяемого пользователя
        uss_id = [el['id'] for el in users]#получаем список id существующих пользователей
        index = uss_id.index(val_id)#получаем индекс существующего пользователя по значению id их входящего json
        users[index] = update_user# присваиваем ключу user_id новое значение
        logger.info(f'PUT: {users}')  # записываем изменения в лог
        return update_user
    except ValueError as e:# если пользователь не найден
        logger.error(f'PUT: {e}')
        raise HTTPException(status_code=404, detail='Not found')

@app.delete("/user/{id}")# функция удаляет элемент с ключом user_id
async def delete_user(id: int) -> dict:
    try:
        uss_id = [el['id'] for el in users]  # получаем список id существующих пользователей
        index = uss_id.index(id)  # получаем индекс существующего пользователя по значению id из входящего json
        del_user = users.pop(index)# удаление элемента по ключу id
        logger.info(f'DELETE: {users}')# пишем изменившийся словарь в лог
        return del_user
    except ValueError as e:
        logger.error(f'DELETE: {e}')
        raise HTTPException(status_code=404, detail='User was not found')

