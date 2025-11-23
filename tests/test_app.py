from http import HTTPStatus


def test_read_root_retornar_ok_e_ola_mundao(client):
    # No nome do teste deve ser o que se espera que aconteça.
    # client = TestClient(app) é o Arrange do teste, mas agora esta na fixture.
    # Instancia o cliente de teste a partir do app

    response = client.get('/')  # Act do teste.
    # Requisição do teste no método e endpoint necessário.

    assert response.status_code == HTTPStatus.OK  # Assert do teste.
    # Validação do código HTTP retornado.
    assert response.json() == {'message': 'Olá, Mundão!'}  # Assert do teste.
    # Validação da resposta retornada.


def test_read_pagina_html_retornar_ok_e_html(client):
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


def test_create_user_retornar_created_e_userpublic(client):
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


def test_read_users_retornar_ok_e_lista_de_usuarios(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'username': 'melissa', 'email': 'melissa@teste.com', 'id': 1}
        ]
    }


def test_read_user_retornar_ok_e_userpublic(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'melissa',
        'email': 'melissa@teste.com',
        'id': 1,
    }


def test_read_user_id_invalido_retornar_not_found_e_mensagem(client):
    response = client.get('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'ID de usuário não encontrado.'}


def test_update_user_retornar_ok_e_userpublic(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'miguel',
            'email': 'miguel@teste.com',
            'password': 'senha_miguel',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'miguel',
        'email': 'miguel@teste.com',
        'id': 1,
    }


def test_update_user_id_invalido_retornar_not_found_e_mensagem(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'sara',
            'email': 'sara@teste.com',
            'password': 'senha_sara',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'ID de usuário não encontrado.'}


def test_delet_user_retornar_ok_e_mensagem(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'O usuário 1 foi deletado do sistema.'
    }


def test_delet_user_id_invalido_retornar_not_found_e_mensagem(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'ID de usuário não encontrado.'}
