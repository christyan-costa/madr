from http import HTTPStatus

from fastapi import FastAPI

from madr.routers import auth, conta, livros, romancistas
from madr.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(conta.router)
app.include_router(livros.router)
app.include_router(romancistas.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Bem-vindo ao Meu Acervo Digital de Romances (MADR)'}
