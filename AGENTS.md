# Repository Guidelines

## Project Structure & Module Organization
This repository defines a Django-based OPD queue management MVP. Core app modules live in `apps/` (`accounts`, `patients`, `queue`, `visits`, `display`, `settings_app`). Shared HTML lives in `templates/`, organized by surface (`base/`, `reception/`, `doctor/`, `display/`). Static assets live in `static/`, infrastructure files in `ops/` and `config/`, and supporting product or engineering docs in the repository root plus `docs/`.

Keep new code close to the owning app. For example, queue rules belong under `apps/queue/`, not in shared utilities unless they are reused across modules.

## Build, Test, and Development Commands
Use the Docker-first workflow unless you are explicitly setting up a local Python environment.

- `make run`: build and start the app stack with Docker Compose.
- `make migrate`: run Django migrations inside the `web` container.
- `make test`: run the Django test suite in the container.
- `docker compose run --rm web python manage.py createsuperuser`: create an admin account.
- `scripts/bootstrap.sh`: bootstrap local setup when extending the environment.

## Coding Style & Naming Conventions
Stay within the locked stack: Django, PostgreSQL, Django templates, HTMX, Tailwind CSS, and minimal Alpine.js. Favor readable server-rendered flows over frontend-heavy abstractions.

Use Python conventions: 4-space indentation, `snake_case` for functions and modules, `PascalCase` for classes, and descriptive app-local names such as `queue_session` or `visit_status`. Keep templates modular and partial-friendly. Avoid framework churn or unnecessary cross-app abstractions.

## Testing Guidelines
Write tests for every queue-rule change. Prioritize model/unit tests, service or business-rule tests, view permission tests, HTMX interaction tests, and smoke tests for critical workflows.

Name tests after observable behavior, for example `test_issue_sequential_tokens` or `test_reception_cannot_open_admin_settings`. Run tests with `make test`.

## Commit & Pull Request Guidelines
Current history uses short, imperative commit messages (`initial`, `Initial commit`). Keep that style, but make messages more specific, such as `Add queue session status validation`.

Pull requests should stay small, describe the workflow or rule being changed, link related issues or docs, and note any schema, permissions, or UI impact. Include screenshots for template or display changes, and update documentation when behavior or scope changes.

## Security & Configuration Notes
Do not commit secrets. Keep environment values in `.env`, keep static/media paths explicit, and verify Caddy and Docker settings when changing deployment behavior.
