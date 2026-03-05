import logging
import os
from logging.config import fileConfig

import alembic_postgresql_enum  # noqa: F401 - needs to be imported to register the enum type with Alembic
import dotenv
from alembic import context
from sqlalchemy import create_engine, pool, text

from otter_db.models import Base

# load environment variables from .env file
dotenv.load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# The list of tables to exclude from migrations. These are managed separately and should not be altered by migrations.
EXCLUDE_TABLES = {"tenants", "alembic_version"}

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    """Exclude certain tables and schemas from migrations."""
    if type_ == "table" and name in EXCLUDE_TABLES:
        return False
    if type_ == "schema":
        return name != "public"
    return True


def get_tenant_schemas(connection) -> list[str]:
    """Read active tenant schemas from the registry."""
    result = connection.scalars(
        text("SELECT schema_name FROM public.tenants WHERE is_active = true")
    ).all()
    return result


def run_migrations_for_schema(connection, schema_name):
    """Run pending migrations for one tenant schema."""
    preparer = connection.dialect.identifier_preparer
    safe_schema = preparer.quote(schema_name)
    connection.execute(text(f"SET search_path TO {safe_schema}"))
    # SQLAlchemy 2.x requires an explicit commit after SET search_path
    connection.commit()

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table="alembic_version",
        # Each schema tracks its own version
        version_table_schema=schema_name,
        include_object=include_object,
    )
    with context.begin_transaction():
        logger.info(f"Running migrations for schema {schema_name}")
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(DB_URL, poolclass=pool.NullPool)

    with engine.connect() as connection:
        tenant_arg = context.get_x_argument(as_dictionary=True).get("tenant")

        schemas = [tenant_arg] if tenant_arg else get_tenant_schemas(connection)

        for schema_name in schemas:
            run_migrations_for_schema(connection, schema_name)


run_migrations_online()
