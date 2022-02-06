from sqlalchemy.orm import Session

from directory.tokens.models import Token


def insert_token(session: Session, token: Token) -> Token:
    session.add(token)
    session.commit()
    return token
