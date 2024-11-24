import uvicorn
from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

messages_db = []


class Message(BaseModel):
    id: int = None
    text: str


@app.get("/users", response_class=HTMLResponse)
async def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("message.html", {"request": request, "messages": messages_db})

@app.get(path="/message/{message_id}")
async def get_message(request: Request, message_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("message.html", {"request": request, "message": messages_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")

@app.post("/message")
async def create_message(message: Message) -> str:
    message_id = len(messages_db)
    messages_db.append(message)
    return f'Message {message_id} created!'

@app.put("/message/message_id")
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.test = message
        return f'Message updated!'
    except IndexError:
        raise  HTTPException(status_code=404, detail='Message not found')

@app.delete("/message/{message_id}")
async def delete_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found')

@app.delete("/")
async def kill_message_all() -> str:
    messages_db.clear()
    return "All messages deleted!"


if __name__ == '__main__':
    uvicorn.run(app)