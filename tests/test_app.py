from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_dunossauro.app import app  # Importa o app definido em app.py


def test_read_root_retornar_ok_e_ola_mundao():
    # No nome do teste deve ser o que se espera que aconteça.
    client = TestClient(app)  # Arrange do teste.
    # Instancia o cliente de teste a partir do app

    response = client.get('/')  # Act do teste.
    # Requisição do teste no método e endpoint necessário.

    assert response.status_code == HTTPStatus.OK  # Assert do teste.
    # Validação do código HTTP retornado.
    assert response.json() == {'message': 'Olá, Mundão!'}  # Assert do teste.
    # Validação da resposta retornada.
