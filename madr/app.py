from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import User
from madr.schemas import Message, UserPublic, UserSchema

app = FastAPI()


T_Session = Annotated[Session, Depends(get_session)]


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Bem-vindo ao Meu Acervo Digital de Romances (MADR)'}


@app.post('/conta', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
            )
    )

    if db_user:
        if db_user.username == user.username:
            # Erro: username já existe
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='conta já consta no MADR'
            )

        if db_user.email == user.email:
            # Erro: email já existe
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='conta já consta no MADR'
            )
    # TO-DO: Aplicar Hash na senha

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
