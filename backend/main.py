from fastapi import FastAPI
from database import Base , engine
from routes.auth import router as auth_router
from routes.tasks import router as tasks_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")
app.include_router(tasks_router, prefix="/tasks")

@app.get("/")
def home():
    return "server successfully running"


