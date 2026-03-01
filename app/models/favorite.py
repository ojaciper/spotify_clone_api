

from sqlalchemy import Column,TEXT, ForeignKey

from app.models.base import Base


class Favorite(Base):
    __tablename__ = "Favorite"
    id=Column(TEXT,primary_key=True)
    user_id = Column(TEXT, ForeignKey("users.id"))
    song_id = Column(TEXT, ForeignKey("songs.id"))