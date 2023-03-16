from fastapi.security import OAuth2PasswordBearer
from fastapi.param_functions import Depends
from providers.token_provider import verify_acess_token
from jose import JWTError
from fastapi import HTTPException, status
from services import UserService
from database.init_db import get_db
from sqlalchemy.orm import Session

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def get_user_logged(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):
    try:
        return "Chegou"
        email = verify_acess_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Inválido")
    
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Inválido")
    
    user_service = UserService()
    user = user_service.get_user_by_email(email)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Inválido")
    
    return user