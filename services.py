from database.models import User, Medication
from database.connection import async_session
from sqlalchemy import delete, select
from fastapi import HTTPException
from exceptions import InvalidUserIdException, InvalidMedicationNameException
import re

class UserService:
    async def delete_user(self, user_id: int):
        async with async_session() as session:
            query = delete(User).where(User.id == user_id)
            result = await session.execute(query)
            await session.commit()
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail='Usuário não encontrado')

    async def create_user(name):
        async with async_session() as session:
            session.add(User(name=name))
            await session.commit()

    async def list_user(self):
        async with async_session() as session:
            query = select(User)
            result = await session.execute(query)
            return result.scalars().all()

class MedicationService:
    async def add_medication(self, user_id: int, name: str):
        if not re.match(r'^[a-zA-Z0-9_-]+$', name):
            raise InvalidMedicationNameException(f"Nome de medicamento inválido: {name}")
        
        if not await self._is_valid_user_id(user_id):
            raise InvalidUserIdException(f"ID de usuário inválido: {user_id}")

        async with async_session() as session:
            session.add(Medication(name=name, user_id=user_id))
            await session.commit()

    async def delete_medication(self, user_id: int, name: str):
        if not await self._is_valid_user_id(user_id):
            raise InvalidUserIdException(f"ID de usuário inválido: {user_id}")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', name):
            raise InvalidMedicationNameException(f"Nome de medicamento inválido: {name}")
        
        async with async_session() as session:
            query = delete(Medication).where(Medication.user_id == user_id).where(Medication.name == name)
            try:
                result = await session.execute(query)
                await session.commit()
                if result.rowcount == 0:
                    raise HTTPException(status_code=404, detail='Medicamento não encontrado!')
            except Exception as e:
                raise HTTPException(status_code=500, detail='Erro ao excluir medicamento!')

    # Verificar se o ID do usuário é válido estando cadastrado no sistema.
    async def _is_valid_user_id(self, user_id: int) -> bool:
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            return result.scalar()
    
    