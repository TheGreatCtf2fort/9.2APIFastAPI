from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Minha FastAPI",
    description="API RESTful desenvolvida com FastAPI",
    version="1.0.0"
)

# Modelo de dados
class User(BaseModel):
    name: str
    age: int
    email: str


users = {}

next_id = 1


@app.get("/")
def hello_world():
    return {
        "message": "Hello World!",
        "status": "success"
    }


@app.get("/api")
def api_info():
    return {
        "name": "Minha FastAPI",
        "version": "1.0.0",
        "description": "API RESTful com FastAPI"
    }


@app.post("/users", status_code=201)
def create_user(user: User):
    global next_id

    user_id = next_id
    users[user_id] = user

    next_id += 1

    return {
        "id": user_id,
        "user": user
    }


@app.get("/users")
def get_users():
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return {
        "id": user_id,
        "user": users[user_id]
    }


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    users[user_id] = user

    return {
        "message": "Usuário atualizado",
        "id": user_id,
        "user": user
    }


@app.patch("/users/{user_id}")
def partial_update_user(user_id: int, user_data: dict):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    current_user = users[user_id].model_dump()

    updated_data = {**current_user, **user_data}

    updated_user = User(**updated_data)

    users[user_id] = updated_user

    return {
        "message": "Usuário atualizado parcialmente",
        "id": user_id,
        "user": updated_user
    }


@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    del users[user_id]

    return {
        "message": "Usuário excluído com sucesso"
    }