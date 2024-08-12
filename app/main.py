from fastapi import FastAPI
from app.api.v1 import auth, category, profile, users, properties  # ...import router lainnya
from app.core.config import settings
from fastapi.security import HTTPBearer
from fastapi_pagination import add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

origins = [
    "http://localhost",  # Ganti dengan origin Laravel Anda
    "http://localhost:8001",
    "http://localhost:3000",
    "http://localhost:4321",
    "https://next-ori.serverdata.my.id"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


add_pagination(app)
security_scheme = [{"bearerAuth": []}]

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["Profile"])
app.include_router(category.router, prefix="/api/v1/category", tags=["Category"])    # Tambahkan ini 
app.include_router(properties.router, prefix="/api/v1/properties", tags=["Properties"])
 

@app.get("/")  # Menambahkan route baru
def read_root():
    return {"Hello": "World"}
# ...include router lainnya
