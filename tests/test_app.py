from http import HTTPStatus

from fastapi_dunossauro.schemas import UserPublic


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


def test_create_user_retonar_conflict_username_e_mensagem(client, user):
    # Criando um registro para Elaine
    response = client.post(
        '/users',
        json={
            'username': 'Melissa',
            'email': 'elaine@test.com',
            'password': 'senha_elaine',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Nome de usuário ou e-mail já existem.'
    }


def test_create_user_retonar_conflict_email_e_mensagem(client, user):
    # Criando um registro para Leonardo
    response = client.post(
        '/users',
        json={
            'username': 'Leonardo',
            'email': 'melissa@test.com',
            'password': 'senha_leonardo',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Nome de usuário ou e-mail já existem.'
    }


def test_read_users_retornar_ok_e_lista_de_usuarios_vazia(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


# Como o banco de dados é "limpo" a cada teste, o teste agora só consegue
# testar o retorno de lista vazia.


def test_read_users_retornar_ok_e_lista_de_usuarios_com_usuarios(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


# Este teste usa a fixture que cria usuário para validar quando
# o banco tem usuários.


def test_read_user_retornar_ok_e_userpublic(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Melissa',
        'email': 'melissa@test.com',
        'id': 1,
    }


def test_read_user_id_invalido_retornar_not_found_e_mensagem(client):
    response = client.get('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'ID de usuário não encontrado.'}


def test_update_user_retornar_ok_e_userpublic(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'Miguel',
            'email': 'miguel@test.com',
            'password': 'senha_miguel',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Miguel',
        'email': 'miguel@test.com',
        'id': 1,
    }


def test_update_user_retonar_conflict_e_mensagem(client, user):
    # Criando um registro para Dirce
    client.post(
        '/users',
        json={
            'username': 'Dirce',
            'email': 'dirce@test.com',
            'password': 'senha_dirce',
        },
    )

    # Alterando o user.username da fixture Melissa
    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'Dirce',
            'email': 'melissa@test.com',
            'password': 'senha_melissa',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Nome de usuário ou e-mail já existem.'
    }


def test_update_user_id_invalido_retornar_not_found_e_mensagem(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'Sara',
            'email': 'sara@test.com',
            'password': 'senha_sara',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'ID de usuário não encontrado.'}


def test_delete_user_retornar_ok_e_mensagem(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'O usuário 1 foi excluído do sistema.'
    }


def test_delete_user_id_invalido_retornar_not_found_e_mensagem(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'ID de usuário não encontrado.'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password}
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
