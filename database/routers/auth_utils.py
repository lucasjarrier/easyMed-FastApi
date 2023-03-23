from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from database.models import User
from services import UserService
from providers.token_provider import verify_acess_token

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/user/login"
)

async def get_usuario_logado(
    token: str = Depends(reusable_oauth2)) -> User:

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    try:
        email = verify_acess_token(token)
    except JWTError:
        raise exception
    
    if not email:
        raise exception
    
    user_service = UserService()
    user = await user_service.get_user_by_email(email)
    if not user:
        raise exception
    return user