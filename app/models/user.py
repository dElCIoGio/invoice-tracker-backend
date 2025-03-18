from typing import Optional

from app.db.mongodb_utils import MongoCrud
from app.schema import user as user_schema


class UserModel(MongoCrud[user_schema.UserDocument]):

    model = user_schema.UserDocument

    async def create_user(self, new_user_data: user_schema.UserCreate) -> user_schema.UserDocument:
        return await self.create(new_user_data.model_dump())

    async def update_user(self, user_id: str, update_data: user_schema.UserUpdate) -> Optional[user_schema.UserDocument]:
        return await self.update(user_id, update_data.model_dump(exclude_none=True))

    async def get_user_by_firebase_uid(self, firebase_uid: str):
        return await user_schema.UserDocument.find_one(user_schema.UserDocument.firebase_uid == firebase_uid)
