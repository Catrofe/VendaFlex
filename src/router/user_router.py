from fastapi import APIRouter, Depends, HTTPException, Request

from src.models.user_model import Password, UserModel, UserModelEdit, UserModelOut
from src.service.middleware.has_auth_role import HasAuthRole
from src.service.user_service import UserService

service = UserService()

router = APIRouter()


@router.post(
    "/user",
    status_code=201,
    response_model=UserModelOut,
    dependencies=[Depends(HasAuthRole(admin=True))],
)
async def create_user(user: UserModel) -> UserModelOut:
    return await service.create_user(user)


@router.get(
    "/user/{user_id}",
    status_code=200,
    response_model=UserModelOut,
    dependencies=[Depends(HasAuthRole())],
)
async def get_user(user_id: int) -> UserModelOut:
    return await service.get_user_by_id(user_id)


@router.get("/user/company/{company_id}")
async def get_users_by_company() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put(
    "/user/{user_id}",
    response_model=UserModelOut,
    status_code=200,
    dependencies=[Depends(HasAuthRole())],
)
async def update_user(
    user_id: int, user_edit: UserModelEdit, request: Request
) -> UserModelOut:
    if (
        request.state.user.id != user_id
        and not request.state.user.admin
        and not request.state.user.company_owner
    ):
        raise HTTPException(status_code=403, detail="You can only update your own user")
    return await service.update_user(user_id, user_edit)


@router.delete(
    "/user/{user_id}",
    response_model=None,
    status_code=204,
    dependencies=[Depends(HasAuthRole())],
)
async def delete_user(user_id: int, request: Request) -> None:
    if (
        request.state.user.id != user_id
        and not request.state.user.admin
        and not request.state.user.company_owner
    ):
        raise HTTPException(status_code=403, detail="You can only delete your own user")
    await service.delete_user(user_id)


@router.patch("/user/{user_id}", response_model=UserModelOut, status_code=200)
async def change_password(
    user_id: int, password: Password, request: Request
) -> UserModelOut:
    if (
        request.state.user.id != user_id
        and not request.state.user.admin
        and not request.state.user.company_owner
    ):
        raise HTTPException(
            status_code=403, detail="You can only change your own password"
        )
    return await service.change_password(user_id, password)
