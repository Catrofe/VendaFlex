import logging
from typing import Optional

from fastapi import HTTPException
from sqlmodel import select

from src.infra.database import Company, Hub, User, get_session_maker
from src.models.hub_model import CompanyMain, CreateNewHub, HubBase, HubEdit, UserMain


class HubRepository:
    def __init__(self) -> None:
        self.session = get_session_maker()

    async def create_hub(self, hub_base: HubBase) -> Hub:
        async with self.session() as session:
            hub = Hub(name=hub_base.name, description=hub_base.description)
            session.add(hub)
            await session.commit()
            await session.refresh(hub)
        return hub

    async def create_company(
        self, request: CompanyMain, hub_id: Optional[int]
    ) -> Company:
        async with self.session() as session:
            company = Company(
                name=request.name, cnpj=request.cnpj, hub_id=hub_id, company_admin=True
            )
            session.add(company)
            await session.commit()
            await session.refresh(company)
        return company

    async def create_user(self, request: UserMain, company_id: Optional[int]) -> User:
        async with self.session() as session:
            user = User(
                username=request.username,
                password=request.password,
                email=request.email,
                phone=request.phone,
                company_id=company_id,
                company_owner=True,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

    async def create_new_hub(self, request: CreateNewHub) -> Hub:
        try:
            hub = await self.create_hub(request.hub)
            company = await self.create_company(request.company, hub.id)
            await self.create_user(request.user, company.id)
            return hub
        except Exception as e:
            logging.info("Error creating new hub, rolling back")
            async with self.session() as session:
                await session.rollback()
            raise HTTPException(status_code=500, detail="Internal server error") from e

    async def get_hub_by_id(self, hub_id: int) -> Optional[Hub]:
        async with self.session() as session:
            query = await session.exec(select(Hub).where(Hub.id == hub_id))
            hub = query.first()
        return hub or None

    async def get_all_hubs(self) -> list[Hub]:
        async with self.session() as session:
            hubs = await session.exec(select(Hub))
            return hubs.all()  # type: ignore

    async def update_hub(self, hub: Hub, request: HubEdit) -> Hub:
        async with self.session() as session:
            changes = request.model_dump(exclude_none=True)
            for key, value in changes.items():
                setattr(hub, key, value)
            await session.commit()
        return hub

    async def delete_hub(self, hub: Hub) -> None:
        async with self.session() as session:
            await session.delete(hub)
            await session.commit()
