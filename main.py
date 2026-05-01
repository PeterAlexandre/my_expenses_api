from fastapi import FastAPI

from app.routes import auth, user

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
