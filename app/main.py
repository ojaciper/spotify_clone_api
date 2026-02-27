from fastapi import FastAPI
from app.models.base import Base
from app.routes import auth
from app.database import engine

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
    

Base.metadata.create_all(engine)