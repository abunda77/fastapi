from fastapi import FastAPI
from app.api.v1 import auth, category, profile, users, properties,regions  # ...import router lainnya
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
    "https://next-ori.serverdata.my.id",
    "https://home.serverdata.my.id",
    "https://bosqu.serverdata.my.id",
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
app.include_router(regions.router, prefix="/api/v1/regions", tags=["Regions"])
 
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@app.get("/")  # Menambahkan route baru
def test_main():
    try:
        return {
            "status_code": 200,
            "status_message": "Connection successful",
            "data": {
                "user": {
                    "name": "John Doe",
                    "email": "johndoe@example.com",
                    "phone": "+123456789",
                    "address": {
                        "street": "123 Main St",
                        "city": "Metropolis",
                        "state": "NY",
                        "zip": "10001"
                    },
                    "created_at": "2024-08-09T12:34:56Z",
                    "updated_at": "2024-08-09T14:56:23Z"
                }
            }
        }
    except Exception as e:
        return {
            "status_code": 500,
            "status_message": "Terjadi kesalahan internal",
            "error": str(e)
        }

# # Fungsi tes terpisah
# def test_root_endpoint():
#     try:
#         response = client.get("/")
#         assert response.status_code == 200
#         assert response.json() == {
#             "status_code": 200,
#             "status_message": "Connection successful",
#             "data": {
#                 "user": {
#                     "name": "John Doe",
#                     "email": "johndoe@example.com",
#                     "phone": "+123456789",
#                     "address": {
#                         "street": "123 Main St",
#                         "city": "Metropolis",
#                         "state": "NY",
#                         "zip": "10001"
#                     },
#                     "created_at": "2024-08-09T12:34:56Z",
#                     "updated_at": "2024-08-09T14:56:23Z"
#                 }
#             }
#         }
#     except AssertionError as ae:
#         print(f"Pengujian gagal: {str(ae)}")
#     except Exception as e:
#         print(f"Terjadi kesalahan saat pengujian: {str(e)}")

# ...include router lainnya
