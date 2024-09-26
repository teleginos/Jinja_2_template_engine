
from typing import List

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    username: str
    age: int


users: List[User] = []

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return templates.TemplateResponse("users.html", {"request": request, "users": users, "selected_user": user})


@app.post("/add_user", response_class=HTMLResponse)
async def post_user(request: Request, username: str = Form(...), age: int = Form(...)) -> HTMLResponse:
    try:
        user_id = users[-1].id + 1 if users else 1
        new_user = User(id=user_id, username=username, age=age)
        users.append(new_user)
        return templates.TemplateResponse("users.html", {"request": request, "users": users})
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid input data")

@app.put("/edit_user/{user_id}")
async def put_user(user_id: int, request: Request, username: str, age: int) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user

    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> User:
    for i, user in enumerate(users):
        if user.id == user_id:
            del_user = users.pop(i)
            return del_user
    raise HTTPException(status_code=404, detail="User was not found")
