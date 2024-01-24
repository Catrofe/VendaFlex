import datetime

import jwt
from fastapi import HTTPException, Request

from src.infra.settings import Settings
from src.models.auth_model import TokenData
from src.service.auth_service import AuthService


class HasAuthRole:
    def __init__(
        self, owner: bool = False, admin: bool = False, refresh: bool = False
    ) -> None:
        self.owner = owner
        self.admin = admin
        self.refresh = refresh
        self.auth_service = AuthService()
        self.settings = Settings()

    def __call__(self, request: Request) -> TokenData:
        try:
            signature = (
                self.settings.REFRESH_SIGNATURE
                if self.refresh
                else self.settings.TOKEN_SIGNATURE
            )
            lee_way = (
                self.settings.REFRESH_TOKEN_EXPIRE_MINUTES if self.refresh else self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            token = request.headers["Authorization"].replace("Bearer ", "")
            token_decoded = jwt.decode(
                token,
                signature,
                algorithms=["HS256"],
                leeway=datetime.timedelta(minutes=lee_way),
            )
            token_data = TokenData(**token_decoded)
            request.state.user = token_data

            if self.owner and not request.state.user.company_owner:
                raise HTTPException(status_code=403)
            if (
                self.admin
                and not request.state.user.admin
                and not request.state.user.company_owner
            ):
                raise HTTPException(status_code=403)
            return token_data

        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401) from e
        except jwt.InvalidSignatureError as e:
            raise HTTPException(status_code=401) from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401) from e
        except Exception as e:
            raise HTTPException(status_code=401) from e
