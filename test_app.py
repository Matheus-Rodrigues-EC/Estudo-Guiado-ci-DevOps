import pytest
import app as app_module

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    resposta = client.get("/")
    assert resposta.status_code == 200

def test_soma_valida(client):
    resposta = client.get("/api/soma?a=10&b=5")
    dados = resposta.get_json()

    assert resposta.status_code == 200
    assert dados["resultado"] == 15.0

def test_desconto_desativado(client, monkeypatch):
    monkeypatch.setattr(
        app_module, "FEATURE_DESCONTO_PROMO", False
    )

    resposta = client.get(
        "/api/desconto?valor=100&porcentagem=25"
    )
    dados = resposta.get_json()

    assert resposta.status_code == 403
    assert dados["flag_status"] is False

def test_desconto_ativado(client, monkeypatch):
    monkeypatch.setattr(
        app_module, "FEATURE_DESCONTO_PROMO", True
    )

    resposta = client.get(
        "/api/desconto?valor=200&porcentagem=25"
    )
    dados = resposta.get_json()

    assert resposta.status_code == 200
    assert dados["Valor com desconto"] == 150.0