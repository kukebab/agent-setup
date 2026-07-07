# data-eng — Project Map

Last updated: YYYY-MM-DD

<!-- ============================================================
     REPLACE WITH YOUR STACK
     ============================================================
     This is a blank template. Replace everything below with your
     actual data pipeline/schema structure and responsibilities.

     When adapting this template to your project:
     1. Replace the directory structure below with yours
     2. Update the file responsibilities to match your setup
     3. Keep the format — file paths, one-line descriptions

     The format is what matters; the specific paths are yours to fill in.
     ============================================================ -->

## Top-level layout

```
<project-root>/
├── <pipelines-dir>/      # ★ this agent owns (dags/, etl/, dbt/, etc.)
├── <warehouse-schemas>/  # ★ this agent owns
└── <app-dirs>/           # NOT this agent's domain
```

## Pipelines / ETL

| Path | Responsibility |
|---|---|
| `<path>` | `<what it does>` |

## Warehouse schemas

| Schema/table | Responsibility |
|---|---|

## Key dependencies

- `<orchestration tool>` (Airflow, Dagster, etc.)
- `<transformation tool>` (dbt, etc.)
- `<warehouse>` (BigQuery, Snowflake, Redshift, etc.)
