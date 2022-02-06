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