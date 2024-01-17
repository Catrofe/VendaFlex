from fastapi import APIRouter

from src.service.user_service import UserService

service = UserService()

router = APIRouter()


@router.post("/user")
async def create_user() -> None:
    raise NotImplementedError()


@router.get("/user/{user_id}")
async def get_user() -> None:
    raise NotImplementedError()


@router.get("/user/{company_id}")
async def get_users() -> None:
    raise NotImplementedError()


@router.put("/user/{user_id}")
async def update_user() -> None:
    raise NotImplementedError()


@router.delete("/user/{user_id}")
async def delete_user() -> None:
    raise NotImplementedError()


@router.patch("/user/{user_id}")
async def patch_user() -> None:
    raise NotImplementedError()
