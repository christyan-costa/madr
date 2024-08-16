from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


# @table_registry.mapped_as_dataclass
# class Romancista:
#     __tablename__ = 'romancistas'

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     name: Mapped[int] = mapped_column(unique=True)

#     # books: Mapped[list['Book']] = relationship(
#     #     init=False, back_populates='book', cascade='all, delete-orphan'
#     # )


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    year: Mapped[str]
    title: Mapped[str]

    romancista_id: Mapped[int]  # = mapped_column(ForeignKey('romancistas.id'))

    # romancista: Mapped[Romancista] = relationship(
    #     init=False, back_populates='books'
    # )
