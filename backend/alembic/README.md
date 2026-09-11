Alembic migration files will be generated here.

After configuring PostgreSQL and .env:

    alembic revision --autogenerate -m "create initial tables"
    alembic upgrade head
