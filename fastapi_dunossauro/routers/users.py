# O FastAPI dispõe da ferramenta routers, que facilita a organização e
# agrupamento de diferentes rotas em uma aplicação. Funciona como um
# "subaplicativo" do FastAPI que pode ser integrado a aplicação principal.
# Isso não só mantém o código organizado e legível, mas também se mostra
# muito útil à medida que a aplicação se expande e rotas são adicionadas.

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi_dunossauro.database import get_session
from fastapi_dunossauro.models import User
from fastapi_dunossauro.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fastapi_dunossauro.security import get_current_user, get_password_hash

# O parâmetro prefix ajuda a agrupar todos os endpoints relacionados
# aos usuários, ou seja, separamos o que é do "domínio" users.
# O uso da tag 'users' contribui para a organização e
# documentação automática no swagger.
router = APIRouter(prefix='/users', tags=['users'])

CurrentUser = Annotated[User, Depends(get_current_user)]
Session = Annotated[Session, Depends(get_session)]


# Utiliza-se @router ao invés de @app para definir estas rotas.
# Com o prefixo definido no router, os paths dos endpoints se tornam mais
# simples e diretos. Ao invés de '/users/{user_id}', por exemplo,
# usamos apenas '/{user_id}'.


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
# Nesta rota, o response_model garante os dados e formato da resposta.
def create_user(user: UserSchema, session: Session):
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
                detail='Nome de usuário ou e-mail já existem.',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Nome de usuário ou e-mail já existem.',
            )

    # Define resposta, caso já exista o username ou email.
    # Boa prática de segurança é informar o mínimo possível, por isso
    # as duas mensagens estão iguais.

    hashed_password = get_password_hash(user.password)
    # hashed_password recebe a senha criptografada.

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,  # A senha criptogra é armazenada no DB.
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    # Se passa na validação, novo usuário é criado no banco de dados.
    # Refresh é usado no final para trazer os outros dados do usuário.

    return db_user


@router.get('/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users(
    session: Session,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()]
):
    # offset permite pular um número específico de registros antes de começar
    # a buscar, o que é útil para implementar a navegação por páginas.
    # limit define o número máximo de registros a serem retornados, permitindo
    # que você controle a quantidade de dados enviados em cada resposta.
    # filter_users invoca o Query Parameters do schema FilterPage.
    users = session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    ).all()
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def read_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para esta ação.',
        )

    db_user = session.scalar(select(User).where(User.id == user_id))

    return db_user


@router.put('/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para esta ação.',
        )

    # Se o usuário logado tiver permissão, a atualização é executada.
    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)
        session.add(current_user)
        session.commit()
        session.refresh(current_user)

        return current_user

    # Porém, se tentar repetir username ou email já utilizados,
    # é barrado com Integrity Error (Conflict).
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nome de usuário ou e-mail já existem.',
        )


@router.delete('/{user_id}', response_model=Message, status_code=HTTPStatus.OK)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para esta ação.',
        )

    # Um ponto interessante com a validação de token implementada é que o
    # usuário logado só tem "visualização" sobre ele próprio, porque qualquer
    # tentativa de atuar em outro usuário só informa que ele não tem permissão

    session.delete(current_user)
    session.commit()

    return {'message': f'O usuário {user_id} foi excluído do sistema.'}
