from http import HTTPStatus

from fastapi_dunossauro.schemas import UserPublic
from fastapi_dunossauro.security import create_access_token


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


# O test_read_users_retornar_ok_e_lista_de_usuarios_vazia não é mais
# necessário, porque com o endpoint protegido pro token, só é possível chamar
# a rota se tiver um usuário para gerar o token.

# Este teste usa a fixture que cria usuário para validar quando
# o banco tem usuários.
def test_read_users_retornar_ok_e_lista_de_usuarios(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_retornar_ok_e_userpublic(client, user, token):
    response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Melissa',
        'email': 'melissa@test.com',
        'id': user.id,
    }


def test_read_user_retornar_forbidden_e_mensagem(client, user, token):
    response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Você não tem permissão para esta ação.'
    }


# O test_read_user_id_invalido_retornar_not_found_e_mensagem não é mais
# necessário, porque com o endpoint protegido pro token, só é possível chamar
# a rota se tiver um usuário para gerar o token.


def test_update_user_retornar_ok_e_userpublic(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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
        'id': user.id,
    }


def test_update_user_retonar_conflict_e_mensagem(client, user, token):
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
        headers={'Authorization': f'Bearer {token}'},
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


def test_delete_user_retornar_ok_e_mensagem(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': f'O usuário {user.id} foi excluído do sistema.'
    }


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password}
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_get_current_user_not_found__exercicio(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Não foi possível validar as credenciais informadas.'
    }


def test_get_current_user_does_not_exists__exercicio(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Não foi possível validar as credenciais informadas.'
    }
