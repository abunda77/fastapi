import sys
import os

# Tambahkan path ke PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    #assert response.json() == {"msg": "Hello World"}

# ... (tes lainnya)
#def test_users():
 #   response = client.get("/api/v1/users")
  #  assert response.status_code == 200
    #assert response.json() == {"msg": "Hello World"}

# ... (tes lainnya untuk endpoint yang berbeda)
