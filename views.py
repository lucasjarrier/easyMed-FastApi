from typing import List
from fastapi import APIRouter, Depends, Form, HTTPException
from schemas import *
from services import UserService, MedicationService
from database.models import User
from database.routers.auth_utils import get_usuario_logado

user_router = APIRouter(prefix='/user')
assets_router = APIRouter(prefix='/assets')
medication_router = APIRouter(prefix='/medication')

@user_router.post('/create', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def user_create(user_input: UserCreateInput):
    try:
        await UserService.create_user(name=user_input.name, email=user_input.email, password=user_input.password)
        return StandardOutput(message='Usuário Criado com Sucesso!')
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@user_router.delete('/delete/{user_id}', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def user_delete(user_id: int):
    try:
        user_service = UserService()
        await user_service.delete_user(user_id)
        return StandardOutput(message='Usuário removido com sucesso!')
    except Exception as e:
        raise HTTPException(status_code=400, detail='Erro ao tentar excluir usuário: {}'.format(user_id))
    
@user_router.get('/', response_model=List[UserListOutput], responses={400: {'model': ErrorOutput}})
async def user_list_all():
    try:
        user_service = UserService()
        return await user_service.list_user()
    except Exception as error:
        raise HTTPException(400, detail="Ocorreu um erro ao tentar listar os usuários!")
    
@user_router.get('/{user_id}', response_model=UserListOutput, responses={400: {'model': ErrorOutput}})
async def get_user_by_id(user_id: int, user_logado: User = Depends(get_usuario_logado)):
    try:
        user_service = UserService()
        return await user_service.get_user_by_id(user_id)
    except Exception:
        raise HTTPException(400, detail=f"Ocorreu um erro ao tentar listar o usuário: {user_id}")

@user_router.put('/{user_id}', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def edit_user_by_id(user_id: int, user_input: UserCreateInput):
    try:
        user_service = UserService()
        await user_service.edit_user(user_id, user_input.name)
        return StandardOutput(message=f"Usuário {user_id} atualizado com sucesso!")
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@user_router.post('/login')
async def login_user(username: str = Form(...), password: str = Form(...)):
    try:
        user_service = UserService()
        return await user_service.user_login(username, password)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@medication_router.post('/create', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def medication_create(medication_input: MedicationCreateInput):
    try:
        medication_service = MedicationService()
        await medication_service.add_medication(user_id = medication_input.user_id, name = medication_input.name)
        return StandardOutput(message="Medicação Adicionada com Sucesso!")
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@medication_router.delete('/remove', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def medication_delete(user_id: int, name: str):
    try:
        medication_service = MedicationService()
        await medication_service.delete_medication(user_id, name)
        return StandardOutput(message="Medicação removida do usuário!")
    except Exception as error:
        raise HTTPException(status_code=400, detail="Erro ao tentar excluir medicação do usuário!")