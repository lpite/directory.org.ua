from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from lib.db import db_dependency
from lib.router import APIRouter
from territories import db
from territories.schemas import (
    GetKATOTTGListResponse,
    KATOTTG,
    GetKATOTTGListParams,
    GetKOATUUListResponse,
    GetKOATUUGListParams,
)

router = APIRouter(
    prefix="/api",
    responses={
        200: {"description": "Успішна відповідь"},
        422: {"description": "Декілька або один параметр запиту містить помилку"},
        500: {"description": "Невідома помилка серверу"},
    },
)

_KATOTTG_TAG = "КАТОТТГ"
_KOATUU_TAG = "КОАТУУ"


@router.get(
    "/katottg",
    summary="Список КАТОТТГ",
    tags=[_KATOTTG_TAG],
    response_model=GetKATOTTGListResponse,
)
def get_katottg_list(
    # input parameters
    params: GetKATOTTGListParams = Depends(),
    # dependencies
    session: Session = Depends(db_dependency),
) -> GetKATOTTGListResponse:
    katottg = db.get_katottg_list(
        session=session,
        code=params.code,
        name=params.name,
        level=params.level,
        parent_id=params.parent,
        category=params.category,
        limit=params.limit,
        offset=params.offset,
    )

    has_previous = params.page != 1
    has_next = len(katottg) == params.page_size + 1
    return GetKATOTTGListResponse(
        has_next=has_next,
        has_previous=has_previous,
        page=params.page,
        results=katottg,
    )


@router.get(
    "/katottg/{code}",
    summary="Отримати дані по КАТОТТГ",
    tags=[_KATOTTG_TAG],
    response_model=KATOTTG,
    responses={404: {"description": "Територіальну одиницю не знайдено"}},
)
def get_katottg_detail(code: str, session: Session = Depends(db_dependency)):
    code = code.upper()

    katottg = db.get_katottg(session=session, code=code)
    if not katottg:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Територіальну одиницю не знайдено: {code}",
        )

    return katottg


@router.get(
    "/koatuu",
    summary="Список КОАТУУ",
    tags=[_KOATUU_TAG],
    response_model=GetKOATUUListResponse,
)
def get_koatuu_list(  # input parameters
    params: GetKOATUUGListParams = Depends(GetKOATUUGListParams),
    # dependencies
    session: Session = Depends(db_dependency),
) -> GetKOATUUListResponse:

    koatuu = db.get_koatuu_list(
        session=session,
        code=params.code,
        name=params.name,
        category=params.category,
        katottg_code=params.code,
        katottg_name=params.name,
        katottg_category=params.katottg_category,
        limit=params.limit,
        offset=params.offset,
    )

    has_previous = params.page != 1
    has_next = len(koatuu) == params.page_size + 1
    return GetKOATUUListResponse(
        has_next=has_next,
        has_previous=has_previous,
        page=params.page,
        results=koatuu,
    )


@router.get(
    "/koatuu/{code}",
    summary="Отримати дані по КОАТУУ",
    tags=[_KOATUU_TAG],
    responses={404: {"description": "Територіальну одиницю не знайдено"}},
)
def get_koatuu_detail(code: str, session: Session = Depends(db_dependency)):
    code = code.upper()

    koatuu = db.get_koatuu(session=session, code=code)
    if not koatuu:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Територіальну одиницю не знайдено: {code}",
        )

    return koatuu


@router.get(
    "/territories",
    summary="Список КАТОТТГ",
    deprecated=True,
    tags=[_KATOTTG_TAG],
    response_model=GetKATOTTGListResponse,
)
def get_territory_list(
    # input parameters
    params: GetKATOTTGListParams = Depends(GetKATOTTGListParams),
    # dependencies
    session: Session = Depends(db_dependency),
) -> GetKATOTTGListResponse:
    return get_katottg_list(params=params, session=session)


@router.get(
    "/territories/{code}",
    summary="Отримати дані по КАТОТТГ",
    deprecated=True,
    tags=[_KATOTTG_TAG],
    response_model=KATOTTG,
)
def get_territory_details(code: str, session: Session = Depends(db_dependency)):
    return get_katottg_detail(code, session=session)
