from datetime import datetime
from typing import List, Optional

from beanie import Document, Indexed
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from pymongo import IndexModel

from app.db.object_id import PyObjectId
from app.schema.document_id import DocumentId
from app.utils.helpers import make_optional_model


class ClientBase(BaseModel):
    name: str
    email: EmailStr = Field(..., description="Client's unique email")
    company: str = Field(..., description="Company name")
    total_invoices: Optional[int] = Field(default=0, description="Total number of invoices")
    outstanding_amount: Optional[float] = Field(default=0.0, description="Total outstanding amount")
    last_invoice_date: Optional[datetime] = Field(None, description="Last invoice date (YYYY-MM-DD)")
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

ClientUpdate = make_optional_model(ClientBase)

class Client(ClientBase, DocumentId):

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class ClientDocument(Client, Document):
    email: Indexed(EmailStr, unique=True, name="idx_email")
    company: Indexed(str, name="idx_company")
    last_invoice_date: Indexed(datetime, name="idx_last_invoice_date")
    outstanding_amount: Indexed(float, name="idx_outstanding_amount")

    class Settings:
        name = "clients"
        bson_encoders = {ObjectId: str}
        indexes = [
            IndexModel(
                "email",
                unique=True,
                name="idx_email"
            ),
            IndexModel(
                "company",
                name="idx_company"
            ),
            IndexModel(
                "last_invoice_date",
                name="idx_last_invoice_date"
            ),
            IndexModel(
                "outstanding_amount",
                unique=True,
                name="idx_outstanding_amount"
            )
        ]
