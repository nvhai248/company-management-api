from typing import Union

from fastapi import FastAPI
from routes import author, auth

app = FastAPI()

app.include_router(author.router)
app.include_router(auth.router)


@app.get("/")
async def health_check():
    return "Oh my god, it running!"
