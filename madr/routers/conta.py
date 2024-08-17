from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import User
from madr.schemas import Message, UserPublic, UserSchema
from madr.security import get_current_user, get_password_hash, sanitize_string

router = APIRouter(prefix='/conta', tags=['contas'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
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


@router.put('/{user_id}', response_model=UserPublic)
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


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, current_user: T_CurrentUser, session: T_Session):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Não autorizado'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
