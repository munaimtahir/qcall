# Queue Management MVP (QCall)

Single-doctor OPD queue management web app built with Django monolith architecture, server-rendered templates, HTMX actions, Tailwind-based UI, PostgreSQL-ready deployment, and PWA metadata.

## Implemented modules
- `accounts`: login/logout, role-based user model (`admin`, `reception`, `doctor`)
- `patients`: patient registry, search (mobile/MR/name), patient detail + visit history
- `queue`: daily queue session, tokening, queue state transitions, reception/doctor dashboards
- `visits`: visit lifecycle records and constraints
- `display`: public read-only live token display
- `settings_app`: clinic and queue behavior settings + daily reset

## Core workflows implemented
- Reception searches returning patient, adds existing/new patient to queue.
- Tokens issue sequentially inside the active daily session.
- Doctor can call next, mark done, and skip.
- Queue supports urgent/cancel/requeue actions.
- Visit history persists across daily resets.
- Public display auto-refreshes current + next tokens.

## Core routes
- `/login/`, `/logout/`
- `/reception/`
- `/doctor/`
- `/patients/`, `/patients/<id>/`, `/patients/search/`
- `/queue/*` action and partial endpoints
- `/display/`, `/display/partials/panel/`
- `/settings/`, `/settings/queue/reset/`
- `/manifest.webmanifest`, `/service-worker.js`

## Local development (virtualenv)
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp .env.example .env`
5. `USE_SQLITE=1 python manage.py migrate`
6. `USE_SQLITE=1 python manage.py runserver`

## Docker run
1. `make run`
2. App via Caddy on `http://localhost:${CADDY_HTTP_PORT}` (from `.env`; set to `0` for random host port)
3. Create admin: `docker compose run --rm web python manage.py createsuperuser`
4. Optional role seed: `docker compose run --rm web python manage.py seed_users`

## Tests
- Local sqlite test run: `USE_SQLITE=1 python manage.py test`
- Docker test run: `make test`
- PostgreSQL parity test run: `docker compose exec -T -e FORCE_POSTGRES_TESTS=1 -e USE_SQLITE=0 web python manage.py test`
