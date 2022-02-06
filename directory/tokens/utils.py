import logging

from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from directory.lib.db import db_dependency
from directory.tokens import db

TokenHeader = APIKeyHeader(name="Token", auto_error=False)


def check_header_token(
    secret: str | None = Depends(TokenHeader),
    session: Session = Depends(db_dependency),
) -> None:
    if not secret:
        logging.warning("No token in header", extra={'secret': secret})

    token = db.get_token(session=session, secret=secret)
    if token is None:
        logging.warning("Request with bad token", extra={"secret": secret})
        # raise HTTPException(
        #     status_code=HTTPStatus.UNAUTHORIZED,
        #     detail="Invalid API Key",
        # )
