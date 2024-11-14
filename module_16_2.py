from fastapi import FastAPI, Path
import uvicorn
from typing import Annotated


app = FastAPI()


@app.get("/user/{user_id}")
async def get_user(user_id: int=Path(ge=1, le=100, description='Enter User ID', example=1)) -> dict:
    return {"message": f"Вы вошли как пользователь № {user_id}"}

@app.get("/user/{username}/{age}")
async def user_param(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                     age: int=Path(ge=18, le=120, description='Enter age', example=24)) -> dict:
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")