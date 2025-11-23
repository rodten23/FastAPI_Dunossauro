# No models.py definimos os modelos de dados que definem a estrutura de como
# os dados serão armazenados no banco de dados.

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import (
    Mapped, mapped_as_dataclass, mapped_column, registry
)

table_registry = registry()


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'
    # __tablename__ é a tabela no banco de dados relacionada com dados abaixo.

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

# Mapped referencia o atributo Python (e seu tipo) que será mapeado para uma
# coluna específica em uma tabela do banco de dados.
# Já a função mapped_column define propriedades daquela coluna, tanto a nível
# do Python, como a nível de tabela no banco de dados.
