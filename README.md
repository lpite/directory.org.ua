# directory.org.ua



# Migrations
Autogenerate migration
```shell
docker compose run --rm alembic revision --autogenerate -m "Init tables"
```

# Load data
```shell
docker compose run --rm commands territories load all
```

# Update dependencies
```shell
docker compose run --rm pip-compile
```

# Update KATOTTG on dokku host
```shell
dokku run directory.org.ua python -m directory.commands territories load katottg
```