from typing import Optional

from pydantic import EmailStr

from app.db.mongodb_utils import MongoCrud
from app.schema import client as client_schema


class ClientModel(MongoCrud[client_schema.ClientDocument]):
    model = client_schema.ClientDocument

    async def create_client(self, new_client_data: client_schema.ClientCreate) -> client_schema.ClientDocument:
        return await self.create(new_client_data.model_dump())

    async def update_client(self, client_id: str, update_data: client_schema.ClientUpdate) -> Optional[client_schema.ClientDocument]:
        return await self.update(client_id, update_data.model_dump(exclude_none=True))

    async def get_client_by_email(self, email: EmailStr) -> client_schema.ClientDocument:
        return await client_schema.ClientDocument.find_one(client_schema.ClientDocument.email == email)


