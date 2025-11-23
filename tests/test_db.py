from sqlalchemy import select

from fastapi_dunossauro.models import User


def test_create_user(session):
    new_user = User(
        username='miguel', password='senha_miguel', email='miguel@teste.com'
    )
    session.add(new_user)
    # .add adiciona o usuário à sessão, mas não ao banco de dados ainda.
    session.commit()
    # .commit salva as informações que estão na sessão no banco de dados.
    user = session.scalar(select(User).where(User.username == 'miguel'))
    # .scalar efetua uma consulta, retornando o primeiro resultado encontrado
    # e o converte para o objeto do SQLAlchemy usando a class User.
    assert user.username == 'miguel'
