import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.middleware.auth_middleware import auth_middleware
import cloudinary
import cloudinary.uploader

from app.models.favorite import Favorite
from app.models.song import Song
from app.schema.favorite_song import FavoriteSong

router = APIRouter()

cloudinary.config(
    cloud_name="dhtqaksb6",
    api_key="696444832926426",
    api_secret="2TYVBUs6N3c5zx_X6AoUwDyutkQ",
)


@router.post("/upload", status_code=201)
def upload_song(
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    song_name: str = Form(...),
    artist: str = Form(...),
    hex_code: str = Form(...),
    db: Session = Depends(get_db),
    auth_dict=Depends(auth_middleware),
):
    song_id = str(uuid.uuid4())
    song_res = cloudinary.uploader.upload(
        song.file, resource_type="auto", folder=f"songs/{song_id}"
    )
    print(song_res["url"])
    thumbnail_res = cloudinary.uploader.upload(
        thumbnail.file, resource_type="image", folder=f"songs/{song_id}"
    )
    print(thumbnail_res["url"])
    new_song = Song(
        id=song_id,
        song_name=song_name,
        artist=artist,
        hex_code=hex_code,
        song_url=song_res["url"],
        thumbnail_url=thumbnail_res["url"],
    )
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song


@router.get("/song")
def songs(db: Session = Depends(get_db), auth_details=Depends(auth_middleware)):
    print(auth_details)
    song = db.query(Song).all()
    return song



@router.post("/favorite")
def favorite_song(
    fav_song: FavoriteSong,
    db: Session = Depends(get_db),
    auth_details=Depends(auth_middleware),
):
    user_id = auth_details["uid"]

    song = (
        db.query(Favorite)
        .filter(Favorite.song_id == fav_song.song_id, Favorite.user_id == user_id)
        .first()
    )
    if song:
        db.delete(song)
        db.commit()
        return {"message": False}

    else:
        new_fav = Favorite(
            id=str(uuid.uuid4()), song_id=fav_song.song_id, user_id=str(user_id)
        )
        db.add(new_fav)
        db.commit()
        return{
            "message":True
        }


@router.get("/favorites")
def favorite_songs(db: Session = Depends(get_db), auth_details=Depends(auth_middleware)):
    user_id = auth_details["uid"]
    user_song= db.query(Favorite).filter(Favorite.user_id == user_id).options(joinedload(Favorite.song)).all()
    return user_song