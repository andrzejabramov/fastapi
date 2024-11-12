from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/user/admin")
async def admin() -> dict:
    return {"message": "Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def user(user_id: str) -> dict:
    return {"message": f"Вы вошли как пользователь № {user_id}"}

@app.get("/user")
async def user_param(name: str, age: int) -> dict:
    return {"message": f"Информация о пользователе. Имя: {name}, Возраст: {age}"}

@app.get("/")
async def main() -> dict:
    return {"message": "Главная страница"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")