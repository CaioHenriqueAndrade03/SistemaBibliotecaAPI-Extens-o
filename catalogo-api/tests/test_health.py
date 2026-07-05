import os
import sys

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Verifica se o serviço sobe e responde na rota raiz."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"