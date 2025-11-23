from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


# Trocar o str por EmailStr tanto na UserSchema, quando na UserPublic,
# garante que teremos um email e não apenas uma string.


class UserDB(UserSchema):
    id: int


# O UserDB herda os campos recebidos do UserSchema e adiciona o id.
