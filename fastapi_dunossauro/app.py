from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_dunossauro.schemas import Message, UserPublic, UserSchema

app = FastAPI(title='API FastAPI Kanban')
# Instancia a aplicação FastAPI na variável 'app'.


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():  # Retorna o dict com chave 'message' e valor 'Olá, Mundão!'.
    return {'message': 'Olá, Mundão!'}


'''
Permite acessar o endpoint raiz ('/') pelo método HTTP GET.
Por padrão, o FastAPI retorna o HTTP status code 200 para consultas tipo GET,
mas podemos deixar explícito ao definir a rota.
'''


@app.get('/pagina-html',
         response_class=HTMLResponse,
         status_code=HTTPStatus.OK)
def read_pagina_html():
    return '''
    <html>
        <head>
            <title> Mundão do HTML! </title>
        </head>
        <body>
            <h1> Olá, Mundão do HTML! </h1>
        </body>
    </html>'''


# Na rota '/pagina-html', nossa API retorna uma página HTML ao cliente.

@app.post('/users', response_model=UserPublic, status_code=HTTPStatus.CREATED)
# Nesta rota, o response_model garante os dados e formato da resposta.
# Já o user: UserSchema garante quais dados e formatos são aceitos
# na requisição.
def create_user(user: UserSchema):
    return user
