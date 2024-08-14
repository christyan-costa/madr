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
    get_current_user,
    get_password_hash,
    sanitize_string,
    verify_password,
)

app = FastAPI()


T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


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
                status_code=HTTPStatus.CONFLICT,
                detail='conta já consta no MADR',
            )

        if db_user.email == user.email:
            # Erro: email já existe
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
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


@app.put('/conta/{user_id}', response_model=UserPublic)
def update_user(
    user: UserSchema,
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Não autorizado'
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/conta/{user_id}', response_model=Message)
def delete_user(user_id: int, current_user: T_CurrentUser, session: T_Session):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Não autorizado'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}


@app.post('/auth/token', response_model=Token)
def login_for_access_token(form_data: T_OAuth2Form, session: T_Session):
    user = session.scalar(select(User).where(User.email == form_data.username))

    # Erro 1: usuário inexistente
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou senha incorretos',
        )

    # Erro 2: senha incorreta
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou senha incorretos',
        )

    access_token = create_access_token({'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
