from fastapi import FastAPI
from database import Base , engine
import models
from routes.auth import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router , prefix="/auth")

@app.get("/")
def home():
    return "server successfully running"


