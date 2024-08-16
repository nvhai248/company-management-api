from typing import Union

from fastapi import FastAPI
from routes import author

app = FastAPI()

app.include_router(author.router)

@app.get("/")
async def health_check():
    return "Oh my god, it running!"