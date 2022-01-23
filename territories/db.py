from sqlalchemy.orm import Session
import sqlalchemy as sa
from territories.enums import KATOTTGCategory, KOATUUCategory
from territories.models import KATOTTG, KOATUU


def truncate_katottg(session: Session) -> None:
    session.execute("TRUNCATE katottg;")


def truncate_koatuu(session: Session) -> None:
    session.execute("TRUNCATE koatuu;")


def insert_katottg(session: Session, items: list[KATOTTG]) -> None:
    session.bulk_save_objects(items)


def insert_koatuu(session: Session, items: list[KOATUU]) -> None:
    session.bulk_save_objects(items)


def update_katottg_children_count(session: Session) -> None:
    session.execute(
        """
       UPDATE katottg
       SET children_count = coalesce((
           SELECT count(t.code) as cnt
           FROM katottg t
           WHERE t.parent_id IS NOT NULL
               AND katottg.code = t.parent_id
           GROUP by t.parent_id), 0)
   """
    )


def get_katottg_list(
    session: Session,
    code: str | None,
    name: str | None,
    level: str | None,
    parent_id: str | None,
    category: KATOTTGCategory | None,
    limit: int,
    offset: int,
) -> list[KATOTTG]:

    filters = []
    if code is not None:
        filters.append(KATOTTG.code == code)

    if name is not None:
        filters.append(KATOTTG.name == name)

    if level is not None:
        filters.append(KATOTTG.level == level)

    if parent_id is not None:
        filters.append(KATOTTG.parent_id == parent_id)

    if category is not None:
        filters.append(KATOTTG.category == category)

    return (
        session.execute(
            sa.select(KATOTTG)
            .order_by(KATOTTG.code)
            .limit(limit)
            .where(sa.and_(*filters))
            .offset(offset)
        )
        .scalars()
        .all()
    )


def get_koatuu_list(
    session: Session,
    code: str | None,
    name: str | None,
    category: KOATUUCategory | None,
    katottg_code: str | None,
    katottg_name: str | None,
    katottg_category: KATOTTGCategory | None,
    limit: int,
    offset: int,
) -> list[KATOTTG]:

    filters = []
    if code is not None:
        filters.append(KOATUU.code == code)

    if name is not None:
        filters.append(KOATUU.name == name)

    if category is not None:
        filters.append(KOATUU.category == category)

    if katottg_code is not None:
        filters.append(KOATUU.katottg_code == katottg_code)

    if katottg_name is not None:
        filters.append(KOATUU.katottg_name == katottg_name)

    if katottg_category is not None:
        filters.append(KOATUU.category == katottg_category)

    return (
        session.execute(
            sa.select(KOATUU)
            .order_by(KOATUU.code)
            .limit(limit)
            .where(sa.and_(*filters))
            .offset(offset)
        )
        .scalars()
        .all()
    )


def get_katottg(session: Session, code: str) -> KATOTTG | None:
    return (
        session.execute(sa.select(KATOTTG).where(KATOTTG.code == code))
        .scalars()
        .first()
    )


def get_koatuu(session: Session, code: str) -> KOATUU | None:
    return (
        session.execute(sa.select(KOATUU).where(KOATUU.code == code)).scalars().first()
    )


def get_katottg_roots(session: Session) -> list[KATOTTG]:
    return (
        session.execute(
            sa.select(KATOTTG).order_by(KATOTTG.name).where(sa.and_(KATOTTG.level == 1))
        )
        .scalars()
        .all()
    )


def get_katottg_children(session: Session, code: str) -> list[KATOTTG]:
    return (
        session.execute(
            sa.select(KATOTTG)
            .order_by(KATOTTG.name)
            .where(sa.and_(KATOTTG.parent_id == code))
        )
        .scalars()
        .all()
    )


def get_katottg_search(session: Session, query: str | None) -> list[KATOTTG]:
    if not query:
        return []

    territories = (
        session.execute(
            sa.select(KATOTTG)
            .options(sa.orm.joinedload(KATOTTG.parent))
            .where(
                sa.or_(
                    KATOTTG.name.match(f"%{query}%"),
                    KATOTTG.name.ilike(f"%{query}%"),
                )
            )
        )
        .scalars()
        .all()
    )

    return sorted(territories, key=lambda t: (len(t.name), t.level))
