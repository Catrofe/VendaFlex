from fastapi import APIRouter

from src.service.auth_service import AuthService

router = APIRouter()

service = AuthService()
