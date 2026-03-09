from sqlalchemy import Text, Column,VARCHAR, LargeBinary
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ ="users"
    id = Column(Text, primary_key=True, index=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)
    favorites = relationship("Favorite", back_populates="user")