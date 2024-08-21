from typing import Union

from fastapi import FastAPI
from routes import company, user, task
from routes import auth

app = FastAPI()

app.include_router(company.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(auth.router)


@app.get("/")
async def health_check():
    return "Oh my god, it running!"
