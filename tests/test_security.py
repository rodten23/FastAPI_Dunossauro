from http import HTTPStatus

from jwt import decode

from fastapi_dunossauro.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}  # Dados que serão assinados pelo token JWT.
    token = create_access_token(data)  # Criação do nosso token JWT.

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])
    # Nessa linha é chamanda a função decode da própria biblioteca do jwt e
    # passamos nosso token, o algoritmo que assinou e a nossa secret key.
    # O resultado da função decode deve ser o valor que passamos para a
    # assinatura {'test': 'test'}, adicionado a claim que adicionamos na
    # função create_access_token.
    # Exemplo: {'test': 'test', 'exp': 1736701785}.

    assert decoded['test'] == data['test']
    assert 'exp' in decoded  # Checa se existe a claim exp no token decodado.


def test_jwt_invalid_token_retornar_unauthorized_e_mensagem(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Não foi possível validar as credenciais informadas.'
    }
