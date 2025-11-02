from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_dunossauro.schemas import Message

app = FastAPI()  # Instancia a aplicação FastAPI na variável 'app'.


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
