from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_dunossauro.database import get_session
from fastapi_dunossauro.models import User
from fastapi_dunossauro.schemas import Token
from fastapi_dunossauro.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]


# O /token recebe os dados do formulário através do form_data
# e tenta recuperar um usuário com o email fornecido.
@router.post('/token', response_model=Token, status_code=HTTPStatus.OK)
# A classe OAuth2PasswordRequestForm é uma classe especial do FastAPI que gera
# automaticamente um formulário para solicitar o username (email neste caso) e
# a senha. Este formulário será apresentado automaticamente no Swagger UI e
# Redoc, facilitando a realização de testes de autenticação.
def login_for_access_token(
    form_data: OAuth2Form,
    session: Session,
):
    # Atenção redobrada: conforme a nota anterior, o formulário gerado por
    # OAuth2PasswordRequestForm armazena credendicais do usuário em username.
    # Como usamos email para identifiar o usuário, aqui comparamos username do
    # formulário com o atributo email do modelo User.
    user = session.scalar(select(User).where(User.email == form_data.username))
    # Se o usuário não for encontrado ou a senha não corresponder ao hash
    # armazenado no banco de dados, uma exceção é lançada.
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='E-mail ou senha inválidos.',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='E-mail ou senha inválidos.',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
