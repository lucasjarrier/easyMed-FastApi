from database.models import User, Medication
from database.routers.connection import async_session
from sqlalchemy import delete, select
from fastapi import HTTPException
from exceptions import InvalidUserIdException, InvalidMedicationNameException
from providers.hash_provider import generate_hash, verify_hash
from providers.token_provider import create_acess_token
import re

class UserService:
    async def delete_user(self, user_id: int):
        async with async_session() as session:
            query = delete(User).where(User.id == user_id)
            result = await session.execute(query)
            await session.commit()
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail='Usuário não encontrado')

    async def create_user(name, email, password):
        async with async_session() as session:
            password_cript = generate_hash(password)
            session.add(User(name=name, password=password_cript, email=email))
            await session.commit()

    async def list_user(self):
        async with async_session() as session:
            query = select(User)
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_user_by_id(self, user_id: int):
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            return result.scalar()
    
    async def edit_user(self, user_id: int, user_name: str):
        async with async_session() as session:
            # Verifica se o usuário existe.
            user = await session.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail=f"Usuário {user_id} não encontrado!")
            
            user.name = user_name
            await session.commit()
    
    async def user_login(self, email: str, password: str):
        async with async_session():
            
            user = await self.get_user_by_email(email)
            if not user:
                raise InvalidUserIdException(f"Nenhum Email: {email} cadastrado.")
            
            validPassword = verify_hash(password, user.password)
            
            if  not validPassword:
                raise InvalidUserIdException(f"Senha Incorreta!")
            
            return await self.create_jwt(user)
        
    async def create_jwt(self, user: User):
        async with async_session():
            token = create_acess_token({'sub': user.email})
            return {'acess_token': token, "token_type": "bearer"}

    async def get_user_by_email(self, user_email: str) -> User:
        async with async_session() as session:
            query = select(User).where(User.email==user_email)
            result = await session.execute(query)
            return result.scalars().first()
    
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
    
    