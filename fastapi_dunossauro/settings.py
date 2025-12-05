from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUES: int
    # A constante DATABASE_URL é o endereço do banco de dados.
    # # A constante SECRET_KEY é usada para assinar o token.
    # O algoritmo HS256 é usado para a codificação.
    # Em produção, a SECRET_KEY fica em local seguro e não exposta no código.
