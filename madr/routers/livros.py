from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Book, User
from madr.schemas import BookPublic, BookSchema
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
        select(Book).where(
            (Book.title == sanitized_title)
            & (Book.year == book.year)
            & (Book.romancista_id == book.romancista_id)
        )
    )

    if db_book:
        # Erro: já consta no MADR!
        ...

    db_book = Book(
        title=sanitize_string(book.title),
        year=book.year,
        romancista_id=book.romancista_id,
    )

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book
