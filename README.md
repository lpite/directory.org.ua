# directory.org.ua



# Migrations
Autogenerate migration
```shell
docker compose run alembic revision --autogenerate -m "Init tables"
```

# Load data
```shell
docker compose run commands load-data
```