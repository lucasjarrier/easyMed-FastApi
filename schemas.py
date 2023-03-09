from pydantic import BaseModel

class UserCreateInput(BaseModel):
    name: str

class StandardOutput(BaseModel):
    message: str

class ErrorOutput(StandardOutput):
    detailt: str