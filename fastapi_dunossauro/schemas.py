from pydantic import BaseModel, ConfigDict, EmailStr, Field


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
    model_config = ConfigDict(from_attributes=True)


# Trocar o str por EmailStr tanto na UserSchema, quando na UserPublic,
# garante que teremos um email e não apenas uma string.
# ConfigDict(from_attributes=True) permite a permite o Pydantic lidar com
# os modelos do SQLAlchemy.


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    # É o token em si que representa a sessão do usuário e contém
    # informações sobre ele.
    token_type: str
    # Tipo de autenticação incluída no header de autorização de cada request.
    # token_type mais comum para JWT é "bearer".


# Este schema serve para definir os Query Parameters da rota read_users e
# usando o Field com opção ge impedimos que sejam incluídos valores negativos.
class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=15)
