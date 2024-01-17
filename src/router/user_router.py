from fastapi import APIRouter, HTTPException

from src.service.user_service import UserService

service = UserService()

router = APIRouter()


@router.post("/user")
async def create_user() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


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
