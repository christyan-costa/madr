from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class BookSchema(BaseModel):
    year: int
    title: str
    romancista_id: int


class BookPublic(BookSchema):
    id: int


class RomancistaSchema(BaseModel):
    name: str


class RomancistaPublic(RomancistaSchema):
    id: int
