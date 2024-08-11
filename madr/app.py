from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import User
from madr.schemas import Message, Token, UserPublic, UserSchema
from madr.security import (
    create_access_token,
    get_password_hash,
    sanitize_string,
)

app = FastAPI()


T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


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
                detail='conta já consta no MADR',
            )

        if db_user.email == user.email:
            # Erro: email já existe
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='conta já consta no MADR',
            )

    # Aplicar hash à senha
    hashed_password = get_password_hash(user.password)

    # Sanitizar nome
    sanitized_username = sanitize_string(user.username)

    db_user = User(
        username=sanitized_username, email=user.email, password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.post('/auth/token', response_model=Token)
def login_for_access_token(form_data: T_OAuth2Form, session: T_Session):
    user = session.scalar(select(User).where(User.email == form_data.username))

    # TO-DO ---> Caso de erro 1: usuário inexistente
    # TO-DO ---> Caso de erro 2: senha incorreta

    access_token = create_access_token({'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
