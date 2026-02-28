from fastapi import FastAPI
from app.models.base import Base
from app.routes import auth, song
from app.database import engine

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(song.router, prefix="/song")
    

Base.metadata.create_all(engine)