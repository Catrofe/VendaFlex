from pydantic import BaseModel, Field


class AuthModel(BaseModel):
    email: str
    password: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    token_expires_in: int
    refresh_token_expires_in: int


class TokenData(BaseModel):
    id: int
    username: str
    company_id: int = Field(alias="companyId")
    company_owner: bool = Field(alias="companyOwner")
    admin: bool
    refresh: bool
