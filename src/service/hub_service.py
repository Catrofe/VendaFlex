from fastapi import HTTPException

from src.models.hub_model import CreateNewHub, HubEdit, HubOut
from src.repository.hub_repository import HubRepository
from src.service.BcryptService import BcryptService


class HubService:
    def __init__(self) -> None:
        self._repository = HubRepository()
        self._encoder = BcryptService()

    async def create_hub(self, request: CreateNewHub) -> HubOut:
        request.user.password = self._encoder.hash_password(request.user.password)
        hub = await self._repository.create_new_hub(request)
        return HubOut(**hub.__dict__)

    async def get_all_hubs(self) -> list[HubOut]:
        hubs = await self._repository.get_all_hubs()
        return [HubOut(**hub.__dict__) for hub in hubs]

    async def get_hub_by_id(self, hub_id: int) -> HubOut:
        hub = await self._repository.get_hub_by_id(hub_id)
        if not hub:
            raise HTTPException(status_code=404, detail="Hub not found")
        return HubOut(**hub.__dict__)

    async def update_hub(self, hub_id: int, request: HubEdit) -> HubOut:
        hub_db = await self._repository.get_hub_by_id(hub_id)
        if not hub_db:
            raise HTTPException(status_code=404, detail="Hub not found")
        hub = await self._repository.update_hub(hub_db, request)
        return HubOut(**hub.__dict__)

    async def delete_hub(self, hub_id: int) -> None:
        hub = await self._repository.get_hub_by_id(hub_id)
        if not hub:
            raise HTTPException(status_code=404, detail="Hub not found")
        await self._repository.delete_hub(hub)
