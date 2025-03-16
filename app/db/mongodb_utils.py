from beanie import Document
from bson import ObjectId
from typing import Any, Dict, List, Optional, Type
from datetime import datetime

from app.db.object_id import PyObjectId


def to_object_id(_id: str) -> PyObjectId:
    try:
        _id = PyObjectId(
            ObjectId(_id)
        )
        return _id
    except:
        raise ValueError("Invalid ObjectId")

class ComparingMethods:
    equals="$eq"
    not_equals="$ne"
    greater_than="$gt"
    greater_or_equal="$gte"
    less_than="$lt"
    less_or_equal="$lte"
    in_="$in"
    not_in="$nin"

class MongoCrud:

    model: Type[Document]


    def __init__(self):
        if not hasattr(self, "model") or not issubclass(self.model, Document):
            raise ValueError("A Beanie Document model must be set in the child class.")

    async def create(self, data: Dict[str, Any]) -> Document:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()

        document = self.model(**data)
        return await document.insert()

    async def read_all(self, skip: int = 0, limit: int = 10) -> List[Document]:
        return await self.model.find().skip(skip).limit(limit).to_list()

    async def read_one(self, _id: str) -> Optional[Document]:
        return await self.model.get(_id)

    async def read_by_fields(
            self, filters: Dict[str, Any], skip: int = 0, limit: int = 10
    ) -> List[Document]:

        return await self.model.find(filters).skip(skip).limit(limit).to_list()

    async def update(self, _id: str, data: Dict[str, Any]) -> Optional[Document]:
        document = await self.model.get(_id)
        if not document:
            return None

        for key, value in data.items():
            setattr(document, key, value)

        document.updated_at = datetime.utcnow()
        await document.save()
        return document

    async def delete(self, _id: str) -> bool:
        document = await self.model.get(_id)
        if document:
            await document.delete()
            return True
        return False


# class MongoCrud:
#     def __init__(self, collection_name: str):
#         self.collection_name = collection_name
#
#     async def create(self, db: AsyncIOMotorDatabase, data: Dict[str, Any]) -> Dict[str, Any]:
#
#         data["created_at"] = datetime.now()
#         data["updated_at"] = datetime.now()
#
#         result = await db[self.collection_name].insert_one(data)
#
#         return await self.read_one(db, result.inserted_id)
#
#     async def read_all(self, db: AsyncIOMotorDatabase, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
#         cursor = db[self.collection_name].find({}).skip(skip).limit(limit)
#         documents = []
#         async for doc in cursor:
#             doc["_id"] = str(doc["_id"])
#             documents.append(doc)
#
#         return documents
#
#     async def read_one(self, db: AsyncIOMotorDatabase, _id: str) -> Optional[Dict[str, Any]]:
#         document = await db[self.collection_name].find_one({"_id": to_object_id(_id)})
#         if document:
#             document["id"] = str(document["_id"])
#         return document
#
#     async def read_by_fields(
#             self, db: AsyncIOMotorDatabase, filters: Dict[str, Any], skip: int = 0, limit: int = 10
#     ) -> List[Dict[str, Any]]:
#         """Fetch documents matching specific field values"""
#
#         cursor = db[self.collection_name].find(filters).skip(skip).limit(limit)
#         documents = []
#         async for doc in cursor:
#             doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
#             documents.append(doc)
#
#         return documents
#
#     async def update(self, db: AsyncIOMotorDatabase, _id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
#         data["updated_at"] = datetime.now()
#         await db[self.collection_name].update_one(
#             {"_id": to_object_id(_id)},
#             {
#                 "$set": data,
#             },
#         )
#         return await self.read_one(db, _id)
#
#     async def delete(self, db: AsyncIOMotorDatabase, _id: str) -> bool:
#         result = await db[self.collection_name].delete_one({"_id": to_object_id(_id)})
#         return result.deleted_count > 0
