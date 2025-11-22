from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
# Trocar o str por EmailStr tanto na UserSchema, quando na UserPublic,
# garante que teremos um email e não apenas uma string.
