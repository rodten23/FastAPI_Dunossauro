from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode

SECRET_KEY = 'your_secret_key'
# Provisório aqui para facilitar entendimento e testes.
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
