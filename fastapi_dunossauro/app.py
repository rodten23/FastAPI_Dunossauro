from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_dunossauro.database import get_session
from fastapi_dunossauro.models import User
from fastapi_dunossauro.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='API - Kanban com FastAPI')
# Instancia a aplicação FastAPI na variável 'app'.

database = []  # Banco de dados falso para ir testando a aplicação.


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():  # Retorna o dict com chave 'message' e valor 'Olá, Mundão!'.
    return {'message': 'Olá, Mundão!'}


"""
Permite acessar o endpoint raiz ('/') pelo método HTTP GET.
Por padrão, o FastAPI retorna o HTTP status code 200 para consultas tipo GET,
mas podemos deixar explícito ao definir a rota.
"""


@app.get(
    '/pagina-html', response_class=HTMLResponse, status_code=HTTPStatus.OK
)
def read_pagina_html():
    return """
    <html>
        <head>
            <title> Mundão do HTML! </title>
        </head>
        <body>
            <h1> Olá, Mundão do HTML! </h1>
        </body>
    </html>"""


# Na rota '/pagina-html', nossa API retorna uma página HTML ao cliente.


@app.post('/users', response_model=UserPublic, status_code=HTTPStatus.CREATED)
# Nesta rota, o response_model garante os dados e formato da resposta.
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    # O user: UserSchema garante quais dados e formatos são aceitos
    # na requisição.
    # session... diz que a função get_session será executada antes da execução
    # da função e o valor retornado por get_session será atribuído ao
    # parâmetro session.
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    # Consulta o banco para validar se já existe username ou email informados.
    # A função scalar pode retornar um objeto ou None.

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Este nome de usuário já existe.',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Este e-mail já está sendo usado.',
            )
    # Define resposta, caso já exista o username ou email.

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    # Se passa na validação, novo usuário é criado no banco de dados.
    # Refresh é usado no final para trazer os outros dados do usuário.

    return db_user


@app.get('/users', response_model=UserList, status_code=HTTPStatus.OK)
def read_users(
    offset: int = 0, limit: int = 30, session: Session = Depends(get_session)
):
    # offset permite pular um número específico de registros antes de começar
    # a buscar, o que é útil para implementar a navegação por páginas.
    # limit define o número máximo de registros a serem retornados, permitindo
    # que você controle a quantidade de dados enviados em cada resposta.
    # Os parâmetros offset e limit se tornam Query Parameters da rota.
    users = session.scalars(select(User).offset(offset).limit(limit)).all()
    return {'users': users}
# Nesta rota, listamos os usuários presentes na banco de dados.


@app.get(
    '/users/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK
)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID de usuário não encontrado.',
        )

    return database[user_id - 1]


@app.put(
    '/users/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK
)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID de usuário não encontrado.',
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}', response_model=Message, status_code=HTTPStatus.OK
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID de usuário não encontrado.',
        )

    del database[user_id - 1]

    return {'message': f'O usuário {user_id} foi deletado do sistema.'}
