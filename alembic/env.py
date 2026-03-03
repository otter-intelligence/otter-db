import logging
from logging.config import fileConfig

import alembic_postgresql_enum  # noqa: F401 - needs to be imported to register the enum type with Alembic
from sqlalchemy import engine_from_config, pool, text

from alembic import context
from otter_db.models import Base

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

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# The list of tables to exclude from migrations. These are managed separately and should not be altered by migrations.
EXCLUDE_TABLES = {"tenants", "alembic_version"}


def include_object(object, name, type_, reflected, compare_to):
    return not (type_ == "table" and name in EXCLUDE_TABLES)


def get_tenant_schemas(connection) -> list[str]:
    """Read active tenant schemas from the registry."""
    result = connection.scalars(
        text("SELECT schema_name FROM public.tenants WHERE is_active = true")
    ).all()
    return result


def run_migrations_for_schema(connection, schema_name):
    """Run pending migrations for one tenant schema."""
    connection.execute(text(f"SET search_path TO {schema_name}"))
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        tenant_arg = context.get_x_argument(as_dictionary=True).get("tenant")

        schemas = [tenant_arg] if tenant_arg else get_tenant_schemas(connection)

        for schema_name in schemas:
            run_migrations_for_schema(connection, schema_name)


run_migrations_online()
