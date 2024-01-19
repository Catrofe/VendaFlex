from typing import Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=155)
    email: str = Field(min_length=8, max_length=155)
    phone: str = Field(min_length=10, max_length=20)
    company_id: Optional[int] = None


class UserModelOut(BaseModel):
    id: int
    username: str
    email: str
    phone: str
    company_id: Optional[int] = Field(alias="companyId", default=None)


class UserModelEdit(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company_id: Optional[int] = None
