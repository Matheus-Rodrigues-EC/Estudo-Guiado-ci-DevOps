from app import app


def test_soma():

    cliente = app.test_client()

    resposta = cliente.get("/api/soma?a=5&b=3")

    assert resposta.status_code == 200
    assert resposta.get_json() == {"resultado": 8.0}
