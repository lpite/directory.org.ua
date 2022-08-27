# directory.org.ua

# Start app
```shell
just start
```

# Migrations
Autogenerate migration
```shell
just alembic-autogenerate "Init tables"
```

# Load data
```shell
just commands territories load all
```

# Update dependencies
```shell
just pip-compile
```

# Format code
```shell
just black
```

# Update KATOTTG on dokku host
```shell
dokku run directory.org.ua python -m directory.commands territories load katottg
```