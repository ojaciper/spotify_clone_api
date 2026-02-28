import uuid
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Header
import jwt
from app.middleware.auth_middleware import auth_middleware
from app.models.user import User
from app.schema.user import UserCreate
from app.schema.user import UserLogin
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/signup")
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(
            status_code=400, detail="User with the same email already exist"
        )
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    user_db = User(
        id=str(uuid.uuid4()), name=user.name, email=user.email, password=hashed_pw
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(
            status_code=400, detail="User with this email does not exist!"
        )
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)

    if not is_match:
        raise HTTPException(status_code=400, detail="Incorrect password!")
    token = jwt.encode(
        {"id": user_db.id},
        "password_key",
    )
    return {"token": token, "user": user_db}


@router.get("/")
def current_user(
    db: Session = Depends(get_db),
    user_dict=Depends(auth_middleware),
):
    user = db.query(User).filter(User.id == user_dict["id"]).first()
    if not user:
        raise HTTPException(404,"User not found")
    return user
