from fastapi import FastAPI

from app.routes import auth, category, report, transaction, user

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(transaction.router)
app.include_router(report.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
