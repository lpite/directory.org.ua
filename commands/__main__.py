import typer

from commands import common

app = typer.Typer()


KATOTTG_FILENAME_DEFAULT = "data/2021.12.16.xlsx"
KOATUU_FILENAME_DEFAULT = "data/koatuu_transition.xlsx"


@app.command(name="load-data")
def load_data(
    katottg_filename: str = KATOTTG_FILENAME_DEFAULT,
    koatuu_filename: str = KOATUU_FILENAME_DEFAULT,
) -> None:
    common.load_katottg(filename=katottg_filename)
    common.load_koatuu(filename=koatuu_filename)


@app.command(name="load-katottg")
def load_katottg(filename: str = KATOTTG_FILENAME_DEFAULT):
    common.load_katottg(filename=filename)


@app.command(name="load-katottg")
def load_koatuu(filename: str = KOATUU_FILENAME_DEFAULT):
    common.load_koatuu(filename=filename)


if __name__ == "__main__":
    app()
