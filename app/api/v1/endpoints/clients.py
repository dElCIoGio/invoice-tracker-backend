
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.schema import client as client_schema
from app.models.client import ClientModel

router = APIRouter()
client_model = ClientModel()

@router.get("/{client_id}", response_model=client_schema.Client)
async def get_client(client_id: str):
    client = await client_model.read_one(client_id)
    if not client_model:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )
    return client_schema.Client(**client.model_dump())


@router.post("/", response_model=client_schema.Client)
async def create_client(new_client_data: client_schema.ClientCreate):
    new_client = await client_model.create_client(new_client_data)
    return client_schema.Client(**new_client.model_dump())


@router.delete("/{client_id}", response_model=bool)
async def delete_client(client_id: str):
    if not await client_model.delete(client_id):
        raise HTTPException(
            status_code=400,
            detail="Client not found"
        )
    return JSONResponse({
        "message": f"Client ({client_id}) deleted!",
        "data": True
    })


@router.put("/{client_id}", response_model=client_schema.Client)
async def update_client(client_id: str, update_data: client_schema.ClientUpdate):
    client = await client_model.update_client(client_id, update_data)
    if not client:
        raise HTTPException(
            status_code=400,
            detail=f"Client not found"
        )
    return client_schema.Client(**client.model_dump())


@router.get("/{email}/email", response_model=client_schema.Client)
async def get_client_by_email(email: str):
    client = await client_model.get_client_by_email(email)
    if not client:
        raise HTTPException(
            status_code=400,
            detail=f"Client with the email '{email}' not found"
        )
    return client_schema.Client(**client.model_dump())
