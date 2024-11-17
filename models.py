from pydantic import BaseModel


class User(BaseModel):
    id: int = 0
    username: str
    age: int