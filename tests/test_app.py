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


def test_read_pagina_html_retornar_ok_e_html():
    client = TestClient(app)

    response = client.get('/pagina-html')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
    <html>
        <head>
            <title> Mundão do HTML! </title>
        </head>
        <body>
            <h1> Olá, Mundão do HTML! </h1>
        </body>
    </html>"""
    )


def test_create_user_retornar_created_e_userpublic():
    client = TestClient(app)

    response = client.post(
        '/users',
        json={
            'username': 'melissa',
            'email': 'melissa@teste.com',
            'password': 'senha',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'melissa',
        'email': 'melissa@teste.com',
        'id': 1,
    }
