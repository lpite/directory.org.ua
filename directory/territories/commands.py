import typer
import re
from itertools import islice

import openpyxl

from directory import territories
from directory.lib import db
from directory.lib.utils import chunks
from directory.territories.enums import KATOTTGCategory, KOATUUCategory
from directory.territories.models import KATOTTG, KOATUU
from translitua import translit, UkrainianKMU


app = typer.Typer()
_load_app = typer.Typer()

app.add_typer(_load_app, name="load")

KATOTTG_FILENAME_DEFAULT = "data/2021.12.23.xlsx"
KOATUU_FILENAME_DEFAULT = "data/koatuu_transition.xlsx"


_katottg_regexp = re.compile(r"^UA\d{17}$")
_koatuu_regexp = re.compile(r"^\d{10}$")
_name_regexp = re.compile(r"^[А-ЩЬЮЯҐЄІЇа-щьюяґєії\- ’/.,]+$")


def translit_name(name: str) -> str:
    return translit(src=name, table=UkrainianKMU)


def normalize_name(name: str) -> str:

    name = name.strip()

    # replace latin letter to cyrillic
    name = name.replace("i", "і").replace("I", "І").replace("A", "А")

    # replace single quote to apostrophe
    name = name.replace("'", "’")

    if not _name_regexp.match(name):
        raise ValueError(f'Name is not valid "{name}"')
    return name


def normalize_katottg(code: str) -> str:
    code = code.strip().upper()
    if not _katottg_regexp.match(code):
        raise ValueError(f'Code is not valid KATOTTG "{code}"')
    return code


def normalize_koatuu(code: str) -> str:
    code = code.strip()
    if not _koatuu_regexp.match(code):
        raise ValueError(f'Code is not valid KOATUU "{code}"')
    return code


def _load_katottg(filename: str) -> None:
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active

    _territories = []
    for row in islice(sheet.rows, 3, None):
        if not row or row[0].value is None:
            break
        *levels_cells, category_cell, name_cell = row
        name: str = normalize_name(name=name_cell.value)
        category = KATOTTGCategory.from_value(value=category_cell.value)
        levels: list[str] = [cell.value for cell in levels_cells if cell.value]
        code: str = normalize_katottg(code=levels[-1])

        parent: None | str = None
        if len(levels) > 1:
            parent = normalize_katottg(code=levels[-2])

        territory = KATOTTG(
            code=code,
            name=name,
            name_en=translit_name(name),
            parent_id=parent,
            level=len(levels),
            category=category,
        )
        _territories.append(territory)
        print(territory)

    with db.get_session() as session:
        with session.begin():

            session.execute("TRUNCATE katottg;")
            territories.db.truncate_katottg(session)

            print("KATOTTG bulk insert ...")
            for chunk in chunks(items=_territories, n=5000):
                territories.db.insert_katottg(session, items=chunk)

            print("Update KATOTTG child count...")
            territories.db.update_katottg_children_count(session)

            print("Successfully load KATOTTG data")


def _load_koatuu(filename: str) -> None:
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active

    _territories = []
    for row in islice(sheet.rows, 1, None):
        if not row or row[0].value is None or row[2].value is None:
            break

        code: str = normalize_koatuu(code=row[0].value)
        category: str | None = row[1].value
        name: str = normalize_name(name=row[2].value)
        katottg_code: str = row[3].value
        katottg_category: str = row[4].value
        katottg_name: str = row[5].value

        _category = KOATUUCategory.from_value(category) if category else None

        territory = KOATUU(
            code=code,
            name=name,
            name_en=translit_name(name),
            category=_category,
        )
        if katottg_name is not None:
            territory.katottg_code = normalize_katottg(code=katottg_code)
            territory.katottg_category = KATOTTGCategory.from_value(katottg_category)
            territory.katottg_name = normalize_name(katottg_name)

        _territories.append(territory)
        print(territory)

    with db.get_session() as session:
        with session.begin():

            print("Truncate KOATUU table...")
            territories.db.truncate_koatuu(session)

            print("Bulk insert KOATUU...")
            for chunk in chunks(items=_territories, n=5000):
                territories.db.insert_koatuu(session, items=chunk)

            print("Successfully load KOATUU data")


@_load_app.command(name="all")
def load_data(
    katottg_filename: str = KATOTTG_FILENAME_DEFAULT,
    koatuu_filename: str = KOATUU_FILENAME_DEFAULT,
) -> None:
    _load_katottg(filename=katottg_filename)
    _load_koatuu(filename=koatuu_filename)


@_load_app.command(name="katottg")
def load_katottg(filename: str = KATOTTG_FILENAME_DEFAULT):
    _load_katottg(filename=filename)


@_load_app.command(name="katottg")
def load_koatuu(filename: str = KOATUU_FILENAME_DEFAULT):
    _load_koatuu(filename=filename)
