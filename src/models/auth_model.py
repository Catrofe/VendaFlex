from pydantic import BaseModel


class AuthModel(BaseModel):
    email: str
    password: str


class TokenModel(BaseModel):
    acessToken: str
    refreshToken: str
    tokenType: str = "bearer"
    tokenExpiresIn: int
    refreshTokenExpiresIn: int


class TokenData(BaseModel):
    id: int
    username: str
    company_id: int
    company_owner: bool
    admin: bool
    refresh: bool
