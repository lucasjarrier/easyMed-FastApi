from jose import jwt
from datetime import datetime, timedelta


# CONFIGURATIONS
SECRET_KEY = '4a9bcb34a2b63b5b26be6de2cbb99431'
ALGORITHM = 'HS256'
EXPIRES_IN_MIN = 3000

def create_acess_token(data: dict):
    datas = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MIN)
    
    datas.update({'exp': expiration})
    
    token_jwt = jwt.encode(datas, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def verify_acess_token(token: str):
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    return payload.get('sub')
