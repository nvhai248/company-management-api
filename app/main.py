from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import company, user, task
from routes import auth

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins. Replace with specific origins in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods. Replace with specific methods if needed.
    allow_headers=["*"],  # Allow all headers. Replace with specific headers if needed.
)

app.include_router(company.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(auth.router)


@app.get("/")
async def health_check():
    return "Oh my god, it running!"
