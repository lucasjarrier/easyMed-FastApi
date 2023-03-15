from typing import List
from fastapi import APIRouter, HTTPException
from schemas import (UserCreateInput, StandardOutput, ErrorOutput, MedicationCreateInput, UserListOutput)
from services import UserService, MedicationService

user_router = APIRouter(prefix='/user')
assets_router = APIRouter(prefix='/assets')
medication_router = APIRouter(prefix='/medication')

@user_router.post('/create', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def user_create(user_input: UserCreateInput):
    try:
        await UserService.create_user(name=user_input.name)
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