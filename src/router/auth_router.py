from fastapi import APIRouter, Depends, Request, status

from src.models.auth_model import AuthModel, TokenModel
from src.service.auth_service import AuthService
from src.service.middleware.has_auth_role import HasAuthRole

router = APIRouter()
service = AuthService()


@router.post("/login", response_model=TokenModel)
async def login(body: AuthModel) -> TokenModel:
    return await service.authenticate(body.email, body.password)


@router.post(
    "/logout",
    dependencies=[Depends(HasAuthRole())],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(request: Request) -> None:
    await service.logout(request.state.user.id)


@router.post(
    "/refresh",
    dependencies=[Depends(HasAuthRole(refresh=True))],
    response_model=TokenModel,
)
async def refresh(request: Request) -> TokenModel:
    return await service.refresh_token(request.state.user.id)
