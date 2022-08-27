PYTHON_COMPOSE_RUN := "docker-compose run --rm _python"
BASE_COMPOSE_RUN := "docker-compose run --rm _base"

start: alembic-upgrade
  docker-compose up web

commands *ARGS:
  {{PYTHON_COMPOSE_RUN}} python -m directory.commands {{ARGS}}

alembic *ARGS:
  {{PYTHON_COMPOSE_RUN}} alembic {{ARGS}}

alembic-upgrade:
  {{PYTHON_COMPOSE_RUN}} alembic upgrade heads

alembic-autogenerate MESSAGE:
  {{PYTHON_COMPOSE_RUN}} alembic revision --autogenerate -m "{{MESSAGE}}"

black:
  {{BASE_COMPOSE_RUN}} black .

pip-compile *ARGS:
  {{PYTHON_COMPOSE_RUN}} pip-copmile {{ARGS}}
