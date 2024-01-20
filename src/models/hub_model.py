from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HubBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=155)
    description: str = Field(..., min_length=2, max_length=1000)


class HubEdit(BaseModel):
    name: Optional[str] = Field(..., min_length=2, max_length=155)
    description: Optional[str] = Field(..., min_length=2, max_length=1000)


class HubOut(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime


class CompanyMain(BaseModel):
    name: str = Field(..., min_length=2, max_length=155)
    cnpj: str = Field(..., min_length=14, max_length=14)


class UserMain(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=155)
    email: str = Field(..., min_length=8, max_length=155)
    phone: str = Field(..., min_length=10, max_length=20)
    company_id: int


class CreateNewHub(BaseModel):
    hub: HubBase
    company: CompanyMain
    user: UserMain
