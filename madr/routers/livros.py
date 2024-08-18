from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Book, User
from madr.schemas import BookPublic, BookSchema, BookUpdate, Message
from madr.security import get_current_user, sanitize_string

router = APIRouter(prefix='/livro', tags=['livros'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=BookPublic)
def add_book(
    book: BookSchema, current_user: T_CurrentUser, session: T_Session
):
    sanitized_title = sanitize_string(book.title)

    db_book = session.scalar(
        select(Book).where((Book.title == sanitized_title))
    )

    if db_book:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Livro já consta no MADR'
        )

    db_book = Book(
        title=sanitized_title,
        year=book.year,
        romancista_id=book.romancista_id,
    )

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.delete('/{book_id}', response_model=Message)
def delete_book(book_id: int, current_user: T_CurrentUser, session: T_Session):
    db_book = session.scalar(select(Book).where((Book.id == book_id)))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    session.delete(db_book)
    session.commit()

    return {'message': 'Livro deletado do MADR'}


@router.patch('/{book_id}', response_model=BookPublic)
def update_book(
    book_id: int,
    book: BookUpdate,
    current_user: T_CurrentUser,
    session: T_Session,
):
    
    db_book = session.scalar(
        select(Book).where(Book.title == sanitize_string(book.title))
    )

    if db_book:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Livro já consta no MADR'
        )


    db_book = session.scalar(select(Book).where((Book.id == book_id)))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book
