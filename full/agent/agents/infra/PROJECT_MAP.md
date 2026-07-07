# infra — Project Map

Last updated: YYYY-MM-DD

<!-- ============================================================
     REPLACE WITH YOUR STACK
     ============================================================
     This is a blank template. Replace everything below with your
     actual infra directory structure and responsibilities.

     When adapting this template to your project:
     1. Replace the directory structure below with yours
     2. Update the file responsibilities to match your setup
     3. Keep the format — file paths, one-line descriptions

     The format is what matters; the specific paths are yours to fill in.
     ============================================================ -->

## Top-level layout

```
<project-root>/
├── <infra-dir>/          # ★ this agent owns (terraform/, deploy/, .github/workflows/, etc.)
└── <app-dirs>/           # NOT this agent's domain
```

## CI/CD

| Path | Responsibility |
|---|---|
| `<path>` | `<what it does>` |

## Infra-as-code

| Path | Responsibility |
|---|---|

## Environments

| Environment | Notes |
|---|---|
| `<staging/prod/...>` | `<url, deploy trigger, notes>` |

## Key dependencies

- `<cloud provider>`
- `<IaC tool>`
- `<monitoring/observability stack>`
