from typing import List
from pydantic import BaseModel

class UserCreateInput(BaseModel):
    name: str

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
    medications: List[Medication]

    class Config:
        orm_mode = True