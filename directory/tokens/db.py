from sqlalchemy.orm import Session
import sqlalchemy as sa
from directory.tokens.models import Token


def insert_token(session: Session, token: Token) -> Token:
    session.add(token)
    session.commit()
    return token


def get_token(session: Session, secret: str) -> Token | None:
    return (
        session.execute(sa.select(Token).where(Token.secret == secret))
        .scalars()
        .first()
    )
