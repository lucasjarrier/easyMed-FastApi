from fastapi import APIRouter, HTTPException
from schemas import UserCreateInput, StandardOutput, ErrorOutput
from services import UserService

user_router = APIRouter(prefix='/user')
assets_router = APIRouter(prefix='/assets')

@user_router.post('/create', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def user_create(user_input: UserCreateInput):
    try:
        await UserService.create_user(name=user_input.name)
        return StandardOutput(message='Usuário Criado com Sucesso!')
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@user_router.delete('/delete/{user_id}', response_model=StandardOutput, responses={400: {'model': ErrorOutput}})
async def user_delete(user_id):
    try:
        await UserService.delete_user(user_id)
        return StandardOutput(message='Usuário Removido com Sucesso!')
    except Exception as error:
        raise HTTPException(400, detail='Erro ao tentar excluir Usuário: ' + str(user_id))