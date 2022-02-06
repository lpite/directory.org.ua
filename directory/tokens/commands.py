import secrets

import typer

from directory.lib import db
from directory.lib.utils import get_secret
from directory.tokens.db import insert_token

from directory.tokens.models import Token

app = typer.Typer()


@app.command(name="new")
def new_token(
    comment: str = typer.Option(...),
) -> None:

    with db.get_session() as session:

        token = Token(comment=comment, secret=get_secret())
        token = insert_token(session, token)

        typer.echo(
            f"""
            New token:
            \tID: {token.id}
            \tToken: {token.secret}
        """
        )
