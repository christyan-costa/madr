from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Bem-vindo ao Meu Acervo Digital de Romances (MADR)'}
