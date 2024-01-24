from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.models.auth_model import AuthModel, TokenModel
from src.service.auth_service import AuthService
from src.service.middleware.has_auth_role import HasAuthRole

router = APIRouter()
service = AuthService()


@router.post("/login")
async def login(request: AuthModel) -> TokenModel:
    return await service.authenticate(request.email, request.password)


@router.post("/logout", dependencies=[Depends(HasAuthRole(admin=True))])
async def logout(request: Request) -> None:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.post("/refresh", dependencies=[Depends(HasAuthRole(refresh=True))])
async def refresh() -> None:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
