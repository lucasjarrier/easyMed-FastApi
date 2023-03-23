from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from views import user_router,  assets_router, medication_router

app = FastAPI()
router = APIRouter()

@router.get('/')
def first():
    return 'Hello world!'

app.include_router(prefix='/first', router=router)
app.include_router(user_router)
app.include_router(assets_router)
app.include_router(medication_router)