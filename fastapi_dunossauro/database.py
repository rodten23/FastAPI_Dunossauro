from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_dunossauro.settings import Settings

# create_async_engine cria a engine de conexão assíncrona com o banco de dados
# o qual é chamado com DATABASE_URL='sqlite+aiosqlite:///database.db' no .env
engine = create_async_engine(Settings().DATABASE_URL)


# AsyncSession gerencia a sessão de banco de dados de forma assíncrona.
async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

# O expire_on_commit=False informa ao SQLAlchemy para não expirar os objetos
# carregados após um commit. O comportamento padrão do SQLAlchemy é expirar o
# cache de objetos após um commit, o que pode causar problemas em operações
# assíncronas, pois o objeto pode ser descartado enquanto estamos aguardando
# em outra corrotina.
