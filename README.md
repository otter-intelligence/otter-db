# DB Migration Repo

This repo contains all SQLAlchemy models, Alembic migrations, and database management tooling for our shared PostgreSQL database.

---

## How Tenancy Works

We use a **schema-per-tenant** model. Each customer gets their own PostgreSQL schema (e.g., `tenant_aquaworks`, `tenant_turbin`) 
containing an identical set of tables. A global `public.tenants` registry tracks which schemas exist.

```
mydb/
  public/
    tenants              ← tenant registry
  tenant_aquaworks/
    sensor_data, events, alarms, alembic_version, ...
  tenant_turbin/
    sensor_data, events, alarms, alembic_version, ...
```

### Why schema-per-tenant?

- **Data isolation** — one tenant can never accidentally see another's data
- **Independent backup/restore** per tenant
- **Clean onboarding/offboarding** — provision or drop a schema without touching others
- **Simple migrations** — all schemas are structurally identical, so one Alembic migration chain applies to all of them

### Per-tenant columns

When a specific customer needs a column that others don't, it's added to the shared model as **nullable**, with a comment indicating which tenant uses it. Every schema gets the column; only the relevant tenant populates it.

```python
class SensorData(Base):
    __tablename__ = "sensor_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # Tenant A only
    calibration_offset: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Tenant B only
    firmware_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
```

---

## How Migrations Work

Alembic is configured to run migrations **once per tenant schema** in a loop. Each schema tracks its own migration
version in its own `alembic_version` table.

The migration scripts in `alembic/versions` themselves are written as if they were targeting a single schema.
The Alembic environment takes care of applying them to each tenant in turn.

---
### Provisioning a New Tenant

```bash
just provision-tenant tenant_name
```

This will: register the tenant in `public.tenants` and create their schema. 
This will NOT run any migrations — the new tenant starts with an empty schema.

> **First time setup:** create the `public.tenants` table with `just create-tenants-table`
---

### Making a Schema Change

1. Edit the relevant model in `/models/`
2. Generate a migration: `just alembic-revision message="some change"`
3. **Review the generated file** — autogenerate is a suggestion, not gospel
4. Verify the `downgrade()` function is correct
5. Apply the migration to all tenants: `just alembic-upgrade`

> **Rule:** All schema changes go through Alembic. No manual DDL in production.

---

## Repo Structure

```
alembic/
  env.py              # multi-schema-aware Alembic entrypoint
  versions/           # migration files
scripts/              
    tenants.py        # Helper functions for tenant management
src/
  otter_db/
    models/            # SQLAlchemy models for all tables 
      __init__.py      # re-exports Base and all models
      base.py          # DeclarativeBase + Tenant registry model
      ...
alembic.ini           # Alembic config (DB connection, etc.)
justfile              # Just commands for common tasks
pyproject.toml        # Python dependencies and project config
```

---

## Further Reading
- [Alembic docs](https://alembic.sqlalchemy.org/en/latest/)
