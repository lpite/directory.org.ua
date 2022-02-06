import typer

from directory.territories import commands as territories
from directory.tokens import commands as tokens

app = typer.Typer()
app.add_typer(territories.app, name="territories")
app.add_typer(tokens.app, name="tokens")


if __name__ == "__main__":
    app()
