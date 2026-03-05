# Use PowerShell 5.1 on Windows, bash on Linux/macOS
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
set shell := ["bash", "-cu"]

default:
    @just --list

# ==========================================================
# Tenant Management
# ==========================================================

db_name := env("POSTGRES_DB", "mydb")
db_user := env("POSTGRES_USER", "myuser")
db_password := env("POSTGRES_PASSWORD", "mypassword")
db_host := env("POSTGRES_HOST", "localhost")
db_port := env("POSTGRES_PORT", "5432")
db_url := "postgresql+psycopg2://" + db_user + ":" + db_password + "@" + db_host + ":" + db_port + "/" + db_name

default_tenant := "Aquaworks"

[doc("First time use: create the tenant table in the public schema")]
create-tenants-table:
    @echo "Creating tenant table in the public schema for {{db_host}}"
    @uv run python scripts/tenants.py --db-url {{db_url}} setup

[doc("Provision a new tenant (create a new schema and register it in the tenant table)")]
provision-tenant tenant_name:
    @echo "Provisioning tenant '{{tenant_name}}' with schema 'tenant_{{lowercase(tenant_name)}}' in {{db_host}}"
    @uv run python scripts/tenants.py --db-url {{db_url}} provision \
        --name {{tenant_name}} --schema-name tenant_{{lowercase(tenant_name)}}

[doc("Deprovision a tenant (drop the tenant schema and remove it from the tenant table).
Default behavior is to soft delete the tenant (mark it as deleted in the tenant table but keep the schema and data).
To hard delete the tenant, set the `hard_delete` parameter to true")]
deprovision-tenant tenant_name hard_delete="false":
    @echo "Deprovisioning tenant '{{tenant_name}}' from {{db_host}} (hard delete: {{hard_delete}})"
    @uv run python scripts/tenants.py --db-url {{db_url}} deprovision \
        --schema-name tenant_{{lowercase(tenant_name)}} \
        --confirm {{ if hard_delete == "true" { "--hard-delete" } else { "" } }}

# ==========================================================
# Alembic Migrations
# ==========================================================

[doc("Create a new revison based on the current state of the models.
The target tenant is fixed, given that the tenant schemas are identical in structure, we can use any tenant schema as
the target for generating the migration script.")]
alembic-revision message:
    uv run alembic -x tenant={{default_tenant}} revision -m "{{message}}" --autogenerate

[doc("Upgrade every tenant to the latest revision.")]
alembic-upgrade:
    uv run alembic upgrade head