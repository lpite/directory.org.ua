from fastapi import APIRouter, Depends, Request, Query, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from lib.db import db_dependency
from territories import db

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/", name="territories")
def index(request: Request, session: Session = Depends(db_dependency)):
    territories = db.get_katottg_roots(session)
    context = {"request": request, "territories": territories}
    return templates.TemplateResponse("index.html", context)


@router.get("/territories/search", name="territories-search")
def search(
    request: Request,
    query: str | None = Query(default=None, alias="q"),
    session: Session = Depends(db_dependency),
) -> Response:
    territories = db.get_katottg_search(session, query=query)
    context = {"territories": territories}
    context = {"request": request, "territories": territories, "query": query}
    return templates.TemplateResponse("search.html", context)


@router.get("/territories/{code}", name="territory")
def details(request: Request, code: str, session: Session = Depends(db_dependency)):
    code = code.upper()
    territory = db.get_katottg(session, code=code)
    if not territory:
        raise 404

    children = db.get_katottg_children(session, code=code)
    parent = territory.parent
    context = {
        "territory": territory,
        "children": children,
        "parent": parent,
        "request": request,
    }

    return templates.TemplateResponse("details.html", context)


@router.get('/ads.txt', response_class=PlainTextResponse)
def ads():
    return 'google.com, pub-4422566096376436, DIRECT, f08c47fec0942fa0'
