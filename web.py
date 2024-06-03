import uvicorn
from fastapi import FastAPI

from src.app.routers import payments

app = FastAPI()

if __name__ == "__main__":
    app.include_router(payments.web_router)
    uvicorn.run(app, host="0.0.0.0", port=8000)
