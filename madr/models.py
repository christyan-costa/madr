from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    year: Mapped[str]
    title: Mapped[str]

    romancista_id: Mapped[int] = mapped_column(ForeignKey('romancistas.id'))

    romancistas: Mapped['Romancista'] = relationship(
        init=False, back_populates='livros'
    )


@table_registry.mapped_as_dataclass
class Romancista:
    __tablename__ = 'romancistas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[int] = mapped_column(unique=True)

    livros: Mapped[list['Book']] = relationship(
        init=False, back_populates='romancistas', cascade='all, delete-orphan'
    )
