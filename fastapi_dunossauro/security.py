from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

# A constante SECRET_KEY é usada para assinar o token.
# O algoritmo HS256 é usado para a codificação.
# Em produção, a SECRET_KEY fica em local seguro e não exposta no código.
SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUES = 30
pwd_context = PasswordHash.recommended()
# Cria um contexto de hash de senhas com a recomendação da pwdlib (o argon2).


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
