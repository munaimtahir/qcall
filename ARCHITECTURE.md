# ARCHITECTURE.md

## System style
Django monolith with server-rendered pages and HTMX-powered partial interactions.

## High-level components
- Django app server
- PostgreSQL database
- Tailwind CSS asset pipeline
- HTMX-enhanced templates
- Optional Alpine.js for tiny local interactions
- Caddy reverse proxy
- Dockerized runtime

## Django apps
### accounts
Auth, login/logout, role checks, user management.

### patients
Patient demographic profile and search.

### queue
Daily queue sessions, token generation, ordering rules, queue actions.

### visits
Visit records, status transitions, lightweight history timeline.

### display
Public queue display views.

### settings_app
Operational settings and clinic preferences.

## Rendering strategy
### Full server-rendered pages
- login
- reception dashboard shell
- patient detail/history
- doctor dashboard shell
- display page shell
- settings pages

### HTMX partial endpoints
- live patient search
- add patient to queue
- call next
- mark done
- skip / cancel
- queue list refresh
- current patient card refresh
- display panel refresh

## Realtime strategy
Start with pragmatic near-realtime:
- HTMX-triggered partial replacement after user actions
- auto-refresh every few seconds for doctor/display screens where needed

Avoid websockets in MVP unless clearly required after field testing.

## Security posture
- Role-based access control
- CSRF enabled
- session-based auth acceptable for MVP
- public display route read-only and token-first

## Deployment shape
- app container
- postgres container
- caddy reverse proxy
- named volumes for database and media
