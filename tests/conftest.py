import pytest
from fastapi.testclient import TestClient

from fastapi_dunossauro.app import app  # Importa o app definido em app.py

# O arquivo conftest.py é um arquivo especial reconhecido pelo pytest que
# permite definir fixtures que podem ser reutilizadas em diferentes
# módulos de teste em um projeto, seguindo o o princípio de
# "Não se repita (DRY).


@pytest.fixture
def client():
    return TestClient(app)


# Uma fixture é como uma função que prepara dados
# ou estado necessários para o teste.
