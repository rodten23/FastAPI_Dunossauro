# O arquivo conftest.py é um arquivo especial reconhecido pelo pytest que
# permite definir fixtures que podem ser reutilizadas em diferentes
# módulos de teste em um projeto, seguindo o o princípio de
# "Não se repita (DRY).

from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_dunossauro.app import app  # Importa o app definido em app.py
from fastapi_dunossauro.database import get_session
from fastapi_dunossauro.models import User, table_registry
from fastapi_dunossauro.security import get_password_hash


# Uma fixture é como uma função que prepara dados
# ou estado necessários para o teste.
@pytest.fixture
def client(session):
    def get_session_override():
        return session

    # Função que retorna a fixture session que será usada nos testes.

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    # Sobrescreve a get_session pela fixture session usada nos testes.

    app.dependency_overrides.clear()
    # Limpa a sobrescrita que fizemos no app para usar a fixture de session.


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    # memory cria um banco de dados em memória, que será usado pela sessão
    # de banco de dados para nossos testes.
    # connect_args... desativa a verificação de que o objeto SQLite está sendo
    # usado na mesma thread em que foi criado. Isso permite que a conexão seja
    # compartilhada entre threads diferentes sem levar a erros.
    # poolclass=StaticPool: faz com que a engine use um pool de conexões
    # estático, ou seja, reutilize a mesma conexão para todas as solicitações.
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


@contextmanager
# Uma fixture de contexto permite manipular algum valor no banco de dados.
# Neste caso, toda veze que um registro de model for inserido no banco de
# dados, se ele tiver o campo created_at, este campo será cadastrado conforme
# definido nas funções abaixo.
def _mock_db_time(
    *,
    model,
    created_time=datetime(2025, 11, 15),
    updated_time=datetime(2025, 11, 30),
):
    # Parâmetros após * devem ser chamados nomeados,
    # para ficarem explícitos na função. Ou seja, mock_db_time(model=User).

    def fake_time_hook(mapper, connection, target):
        # Os parâmetros mapper, connection e target são obrigatórios.
        if hasattr(target, 'created_at'):
            target.created_at = created_time

        if hasattr(target, 'updated_at'):
            target.updated_at = updated_time

    # Função para alterar alterar o método created_at do objeto de target.

    event.listen(model, 'before_insert', fake_time_hook)
    # event.listen adiciona um evento relacionado a um model que será passado
    # à função. Esse evento é o before_insert e ele executará
    # uma função (hook) antes de inserir o registro no banco de dados.

    yield created_time, updated_time
    # yield retorna o datetime na abertura do gerenciamento de contexto.

    event.remove(model, 'before_insert', fake_time_hook)
    # event.remove remove o hook dos eventos após o final do gerenciamento
    # de contexto.


@pytest.fixture
def mock_db_time():
    return _mock_db_time


# Fixture que retorna a fixture de contexto para manipular o created_at.


@pytest.fixture
def user(session):
    password = 'senha_melissa'
    user = User(
        username='Melissa',
        email='melissa@test.com',
        password=get_password_hash('senha_melissa')  # Senha criptografada.
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Aqui é feita uma modificação no objeto user (um monkey patch) para
    # adicionar a senha em texto puro.
    # Monkey patching é uma técnica em que modificamos ou estendemos o código
    # em tempo de execução. Neste caso, estamos adicionando um novo atributo
    # clean_password ao objeto user para armazenar a senha em texto puro.
    user.clean_password = password

    return user


# Fixture para criar usuário de teste no banco de dados real.
