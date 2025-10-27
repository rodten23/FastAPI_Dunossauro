from fastapi import FastAPI

app = FastAPI()  # Instancia a aplicação FastAPI na variável 'app'.


@app.get('/')  # Permite acessar o endpoint raiz ('/') pelo método HTTP GET.
def read_root():  # Retorna o dict com chave 'message' e valor 'Olá, Mundão!'.
    return {'message': 'Olá, Mundão!'}
