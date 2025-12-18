from dataclasses import asdict

import pytest
from sqlalchemy import select

from fastapi_dunossauro.models import User


# Testes também podem ser corrotinas assíncronas, porém o pytest não os
# executa em um loop de eventos. Para isso ser feito, temos que indicar
# que um determinado teste é assíncrono. Para isso, usamos a marcação
# @pytest.mark.asyncio.
@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        # Inicia o gerenciador de contexto mock_db_time
        # usando o modelo User como base.
        new_user = User(
            username='miguel',
            password='senha_miguel',
            email='miguel@teste.com',
        )
        # .add adiciona o usuário à sessão, mas não ao banco de dados ainda.
        session.add(new_user)
        # .commit salva as informações que estão na sessão no banco de dados.
        # .commit faz uma chamada ao banco de dados é categorizada como I/O.
        # Logo, essa chamada pode escalonar o async, então usamos await.
        await session.commit()

    # .scalar efetua uma consulta, retornando o primeiro resultado encontrado
    # e o converte para o objeto do SQLAlchemy usando a class User.
    # Outra chamada que depende de I/O, a chamada no banco espera a consulta
    # ser concluída, logo, também usamos await.
    user = await session.scalar(select(User).where(User.username == 'miguel'))

    assert asdict(user) == {
        # Converte user num dicionário para simplificar a validação no teste.
        'id': 1,
        'username': 'miguel',
        'password': 'senha_miguel',
        'email': 'miguel@teste.com',
        'created_at': time[0],
        'updated_at': time[1],
        # Usa o time gerado por mock_db_time para validar o campo created_at.
    }
