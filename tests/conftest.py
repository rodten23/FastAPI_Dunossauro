import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_dunossauro.app import app  # Importa o app definido em app.py
from fastapi_dunossauro.models import table_registry

# O arquivo conftest.py é um arquivo especial reconhecido pelo pytest que
# permite definir fixtures que podem ser reutilizadas em diferentes
# módulos de teste em um projeto, seguindo o o princípio de
# "Não se repita (DRY).


@pytest.fixture
def client():
    return TestClient(app)


# Uma fixture é como uma função que prepara dados
# ou estado necessários para o teste.


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    # memory cria um banco de dados em memória, a partir do qual será criada
    # uma sessão de banco de dados para nossos testes.
    table_registry.metadata.create_all(engine)
    # .metadata.create_all(engine) cria todas as tabelas no banco de dados de
    # teste antes de cada teste que usa a fixture session.

    with Session(engine) as session:
        yield session
        # yield fornece uma instância de Session que será injetada em cada
        # teste que solicita a fixture session.

    table_registry.metadata.drop_all(engine)
    # .drop_all(engine) limpa as tabelas do banco de dados a cada teste.
    engine.dispose()
    # .dispose fecha todas as conexões abertas associadas ao engine.
