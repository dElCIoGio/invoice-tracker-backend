from typing import List, Optional

from beanie import Document, Indexed
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from app.db.object_id import PyObjectId
from app.schema.document_id import DocumentId
from app.utils.helpers import partial_model


class UserBase(BaseModel):
    firebase_uid: str


class UserCreate(UserBase):
    pass


@partial_model
class UserUpdate(UserBase):
    pass

class User(UserBase, DocumentId):

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class UserDocument(User, Document):
    firebase_uid: Indexed(str, unique=True)


    class Settings:
        name = "users"
        bson_encoders = {ObjectId: str}

