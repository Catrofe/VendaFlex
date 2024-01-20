from fastapi import APIRouter

from src.models.hub_model import CreateNewHub, HubEdit, HubOut
from src.service.hub_service import HubService

router = APIRouter()

service = HubService()


@router.post("/hub", response_model=HubOut, status_code=201)
async def create_hub(hub: CreateNewHub) -> HubOut:
    return await service.create_hub(hub)


@router.get("/hub/{hub_id}", response_model=HubOut, status_code=200)
async def get_hub(hub_id: int) -> HubOut:
    return await service.get_hub_by_id(hub_id)


@router.get("/hub", response_model=list[HubOut], status_code=200)
async def get_all_hub() -> list[HubOut]:
    return await service.get_all_hubs()


@router.put("/hub/{hub_id}", response_model=HubOut, status_code=200)
async def update_hub(hub_id: int, hub: HubEdit) -> HubOut:
    return await service.update_hub(hub_id, hub)


@router.delete("/hub/{hub_id}", response_model=None, status_code=204)
async def delete_hub(hub_id: int) -> None:
    return await service.delete_hub(hub_id)
