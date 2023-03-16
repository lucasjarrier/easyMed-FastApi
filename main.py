from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from views import user_router,  assets_router, medication_router

app = FastAPI()
router = APIRouter()

origins = ['http://localhost:8080']

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get('/')
def first():
    return 'Hello world!'

app.include_router(prefix='/first', router=router)
app.include_router(user_router)
app.include_router(assets_router)
app.include_router(medication_router)