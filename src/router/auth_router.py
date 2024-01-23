from fastapi import APIRouter, HTTPException, status

from src.models.auth_model import AuthModel, TokenModel
from src.service.auth_service import AuthService

router = APIRouter()
service = AuthService()


@router.post("/login")
async def login(request: AuthModel) -> TokenModel:
    return await service.authenticate(request.email, request.password)


@router.post("/logout")
async def logout() -> None:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
