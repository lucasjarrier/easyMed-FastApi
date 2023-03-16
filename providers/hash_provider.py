from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])

def verify_hash(password, password_cript):
    return pwd_context.verify(password, password_cript)

def generate_hash(password):
    return pwd_context.hash(password)
