from sqlalchemy import Column,TEXT, ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship


class Favorite(Base):
    __tablename__ = "Favorite"
    id=Column(TEXT,primary_key=True)
    user_id = Column(TEXT, ForeignKey("users.id"))
    song_id = Column(TEXT, ForeignKey("songs.id"))
    song = relationship("Song")
    user = relationship("User",back_populates='favorites')