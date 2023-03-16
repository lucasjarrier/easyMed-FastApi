from typing import List
from pydantic import BaseModel

class UserCreateInput(BaseModel):
    name: str
    email: str
    password: str

class StandardOutput(BaseModel):
    message: str

class ErrorOutput(StandardOutput):
    detailt: str

class MedicationCreateInput(BaseModel):
    name: str
    user_id: int

class Medication(BaseModel):
    id: int
    name: str
    user_id: int

    class Config:
        orm_mode = True
class UserListOutput(BaseModel):
    id: int
    name: str
    email: str
    password: str
    medications: List[Medication]

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginOutput(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True