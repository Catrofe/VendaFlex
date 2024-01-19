from fastapi import APIRouter, HTTPException

from src.models.user_model import UserModel, UserModelEdit, UserModelOut
from src.service.user_service import UserService

service = UserService()

router = APIRouter()


@router.post("/user", status_code=201, response_model=UserModelOut)
async def create_user(user: UserModel) -> UserModelOut:
    return await service.create_user(user)


@router.get("/user/{user_id}", status_code=200, response_model=UserModelOut)
async def get_user(user_id: int) -> UserModelOut:
    return await service.get_user_by_id(user_id)


@router.get("/user/{company_id}")
async def get_users_by_company() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/user/{user_id}", response_model=UserModelOut, status_code=200)
async def update_user(user_id: int, user_edit: UserModelEdit) -> UserModelOut:
    return await service.update_user(user_id, user_edit)


@router.delete("/user/{user_id}")
async def delete_user() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.patch("/user/{user_id}")
async def patch_user() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")
