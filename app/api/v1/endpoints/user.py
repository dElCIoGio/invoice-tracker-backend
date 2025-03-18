
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.schema import user as user_schema
from app.models.user import UserModel

router = APIRouter()
user_model = UserModel()

@router.get("/{user_id}", response_model=user_schema.User)
async def get_user(user_id: str):
    user = await user_model.read_one(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user_schema.User(**user.model_dump())


@router.post("/", response_model=user_schema.User)
async def create_user(new_user_data: user_schema.UserCreate):
    new_user = await user_model.create_user(new_user_data)
    return user_schema.User(**new_user.model_dump())


@router.put("/{user_id}", response_model=user_schema.User)
async def update_user(user_id: str, update_data: user_schema.UserUpdate):
    user = await user_model.update_user(user_id, update_data)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    return user_schema.User(**user.model_dump())


@router.delete("/{user_id}", response_model=bool)
async def delete_user(user_id: str):
    if not await user_model.delete(user_id):
        raise HTTPException(
            status_code=400,
            detail="Client not found"
        )
    return JSONResponse({
        "message": f"Client ({user_id}) deleted!",
        "data": True
    })

@router.get("/{firebase_uid}/firebase", response_model=user_schema.User)
async def get_user_by_firebase_uid(firebase_uid: str):
    user = await user_model.get_user_by_firebase_uid(firebase_uid)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    return user_schema.User(**user.model_dump())