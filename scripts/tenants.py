import argparse
import logging

from sqlalchemy import create_engine, delete, text, update
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from otter_db.models import Base, Tenant

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def get_engine(db_url: str) -> Engine:
    return create_engine(db_url)


def setup_tenant_table(db_url: str):
    """Create the public.tenants table if it doesn't exist."""
    engine = get_engine(db_url)
    Base.metadata.create_all(engine, tables=[Tenant.__table__])
    logger.info("Tenant table ready.")


def provision_tenant(name: str, schema_name: str, db_url: str):
    """Register tenant and create schema. Run migrations separately."""
    if not schema_name.startswith("tenant_") or not schema_name.isidentifier():
        raise ValueError(f"Invalid schema name: {schema_name}")

    engine = get_engine(db_url)
    with Session(engine) as session, session.begin():
        session.add(Tenant(name=name, schema_name=schema_name))
        session.execute(text(f"CREATE SCHEMA {schema_name}"))

    logger.info(
        f"Tenant '{name}' provisioned at schema '{schema_name}'. Run migrations separately."
    )


def deprovision_tenant(
    schema_name: str, db_url: str, hard_delete: bool = False, confirm: bool = False
):
    """Deactivate or permanently remove a tenant."""
    if not confirm:
        raise ValueError("You must pass --confirm to deprovision a tenant.")

    if hard_delete:
        double_confirm = input(
            f"Type the schema name '{schema_name}' to permanently delete it: "
        )
        if double_confirm != schema_name:
            logger.error("Schema name did not match. Aborting.")
            raise SystemExit(1)

    engine = get_engine(db_url)
    with Session(engine) as session, session.begin():
        if hard_delete:
            session.execute(text(f"DROP SCHEMA {schema_name} CASCADE"))
            session.execute(delete(Tenant).where(Tenant.schema_name == schema_name))
            logger.info(f"Tenant '{schema_name}' permanently deleted.")
        else:
            session.execute(
                update(Tenant)
                .where(Tenant.schema_name == schema_name)
                .values(is_active=False)
            )
            logger.info(f"Tenant '{schema_name}' deactivated.")


def main():
    parser = argparse.ArgumentParser(description="Tenant management CLI")
    parser.add_argument("--db-url", required=True, help="PostgreSQL connection URL")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("setup", help="Create public.tenants table if not exists")

    p_provision = subparsers.add_parser(
        "provision", help="Register a new tenant and create their schema"
    )
    p_provision.add_argument("--name", required=True, help="Human-readable tenant name")
    p_provision.add_argument(
        "--schema-name",
        required=True,
        help="Postgres schema name (must start with 'tenant_')",
    )

    p_deprovision = subparsers.add_parser(
        "deprovision", help="Deactivate or permanently remove a tenant"
    )
    p_deprovision.add_argument(
        "--schema-name", required=True, help="Postgres schema name to deprovision"
    )
    p_deprovision.add_argument(
        "--hard-delete",
        action="store_true",
        help="Permanently drop schema and delete registry entry",
    )
    p_deprovision.add_argument(
        "--confirm",
        action="store_true",
        required=True,
        help="Required to confirm deprovisioning.",
    )

    args = parser.parse_args()

    try:
        if args.command == "setup":
            setup_tenant_table(args.db_url)
        elif args.command == "provision":
            provision_tenant(args.name, args.schema_name, args.db_url)
        elif args.command == "deprovision":
            deprovision_tenant(
                args.schema_name,
                args.db_url,
                hard_delete=args.hard_delete,
                confirm=args.confirm,
            )
    except Exception:
        logger.exception("Command failed.")
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
