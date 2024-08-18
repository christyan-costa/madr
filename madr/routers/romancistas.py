from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Romancista, User
from madr.schemas import Message, RomancistaPublic, RomancistaSchema
from madr.security import get_current_user, sanitize_string

router = APIRouter(prefix='/romancista', tags=['romancistas'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', response_model=RomancistaPublic, status_code=HTTPStatus.CREATED
)
def add_romancista(
    romanc: RomancistaSchema, current_user: T_CurrentUser, session: T_Session
):
    romanc_name = sanitize_string(romanc.name)

    db_romancista = session.scalar(
        select(Romancista).where((Romancista.name == romanc_name))
    )

    if db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já consta no MADR',
        )

    db_romancista = Romancista(name=romanc_name)

    session.add(db_romancista)
    session.commit()
    session.refresh(db_romancista)

    return db_romancista


@router.delete('/{romancista_id}', response_model=Message)
def delete_romancista(
    romancista_id: int, current_user: T_CurrentUser, session: T_Session
):
    db_romancista = session.scalar(
        select(Romancista).where((Romancista.id == romancista_id))
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    session.delete(db_romancista)
    session.commit()

    return {'message': 'Romancista deletado do MADR'}
