from typing import List, Optional

from beanie import Document, Indexed
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from app.db.object_id import PyObjectId
from app.schema.document_id import DocumentId
from app.utils.helpers import partial_model


class ClientBase(BaseModel):
    name: str
    email: EmailStr = Field(..., description="Client's unique email")
    company: str = Field(..., description="Company name")
    total_invoices: Optional[int] = Field(default=0, description="Total number of invoices")
    outstanding_amount: Optional[float] = Field(default=0.0, description="Total outstanding amount")
    last_invoice_date: Optional[str] = Field(None, description="Last invoice date (YYYY-MM-DD)")
    contact_person: str
    phone: str
    address: str
    payment_history: Optional[List[PyObjectId]] = Field(default=[], description="List of payment references")


class ClientCreate(ClientBase):
    """
    name: str
    email: EmailStr
    company: str
    contact_person: str
    phone: str
    address: str
    """
    pass

@partial_model
class ClientUpdate(ClientBase):
    pass

class Client(ClientBase, DocumentId):

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class ClientDocument(Client, Document):
    email: Indexed(EmailStr, unique=True)
    company: Indexed(str)
    last_invoice_date: Indexed(str)
    outstanding_amount: Indexed(float)

    class Settings:
        name = "clients"
        bson_encoders = {ObjectId: str}
        indexes = [
            "email",
            "company",
            "last_invoice_date",
            "outstanding_amount",
        ]
