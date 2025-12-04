from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_dunossauro.database import get_session
from fastapi_dunossauro.models import User

# A constante SECRET_KEY é usada para assinar o token.
# O algoritmo HS256 é usado para a codificação.
# Em produção, a SECRET_KEY fica em local seguro e não exposta no código.
SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUES = 30
pwd_context = PasswordHash.recommended()
# Cria um contexto de hash de senhas com a recomendação da pwdlib (o argon2).

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# create_access_token cria um novo token JWT para autenticar o usuário.
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUES
    )
    # Recebe um dicionário de dados e adiciona o tempo de expiração ao token.
    # Esses dados, em conjunto, formam o payload do JWT.
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    # Usa a biblioteca pyjwt para codificar essas informações em um token JWT,
    # que é então retornado.


# Cria um hash argon2 para o password.
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Verifica se a plain_password é igual à hashed_password
# quando aplicado ao contexto do argon2.
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# get_current_user é responsável por extrair o token JWT do
# header Authorization da requisição, decodificar esse token,
# extrair as informações do usuário e obter finalmente o usuário
# do banco de dados. Se qualquer um desses passos falhar,
# uma exceção será lançada e a requisição será negada.
def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
    # A injeção de oauth2_scheme garante que um token foi enviado.
     # Caso não tenha sido enviado, ele redirecionará a tokenUrl
    # do objeto OAuth2PasswordBearer.
):
    # Como essa operação pode apresentar erros em diversos momentos,
    # foi atribuído um único erro à variável credentials_exception.
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Não foi possível validar as credenciais informadas.',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        # Checa, após o decode do token, se o email está presente no subject.
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception
    # Nessa validação é testada se o token é um token JWT válido.
    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))

    # Checa se o e-mail está presente no banco de dados.
    if not user:
        raise credentials_exception

    return user
