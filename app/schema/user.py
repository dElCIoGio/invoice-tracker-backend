
from beanie import Document, Indexed
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from pymongo import IndexModel

from app.db.object_id import PyObjectId
from app.schema.document_id import DocumentId
from app.utils.helpers import make_optional_model


class UserBase(BaseModel):
    email: EmailStr
    firebase_uid: str
    phone: str
    first_name: str
    last_name: str



class UserCreate(UserBase):
    pass


UserUpdate = make_optional_model(UserBase)


class User(UserBase, DocumentId):

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class UserDocument(Document, UserBase):
    email: Indexed(EmailStr, unique=True, name="idx_email")  # Ensure email is unique
    firebase_uid: Indexed(str, unique=True, name="idx_firebase_uid")

    class Settings:
        name = "users"
        bson_encoders = {ObjectId: str}
        indexes = [
            IndexModel(
                "email",
                unique=True,
                name="idx_email"
            ),
            IndexModel(
                "firebase_uid",
                unique=True,
                name="idx_firebase_uid"
            )
        ]