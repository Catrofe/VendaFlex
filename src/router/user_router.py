from fastapi import APIRouter, HTTPException

from src.models.user_model import UserModel, UserModelOut
from src.service.user_service import UserService

service = UserService()

router = APIRouter()


@router.post("/user", status_code=201, response_model=UserModelOut)
async def create_user(user: UserModel) -> UserModelOut:
    return await service.create_user(user)


@router.get("/user/{user_id}")
async def get_user() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/user/{company_id}")
async def get_users_by_company() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/user/{user_id}")
async def update_user() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/user/{user_id}")
async def delete_user() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.patch("/user/{user_id}")
async def patch_user() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")
