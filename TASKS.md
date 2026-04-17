# TASKS.md

## Stage 0 — Foundation
- [x] Initialize Django project structure
- [x] Add apps: accounts, patients, queue, visits, display, settings_app
- [x] Configure PostgreSQL connection
- [x] Add settings split for dev/prod
- [x] Add Tailwind integration
- [x] Add Dockerfile and docker-compose.yml
- [x] Add Caddy sample config

## Stage 1 — Auth and roles
- [x] Implement login/logout
- [x] Create role model or role field
- [x] Seed admin, reception, doctor users
- [x] Protect routes by role

## Stage 2 — Patients
- [x] Create Patient model
- [x] Add patient admin
- [x] Create patient list/search page
- [x] Create patient create/edit/detail pages
- [x] Implement HTMX search partial

## Stage 3 — Queue core
- [x] Create DailyQueueSession model
- [x] Create Visit model
- [x] Implement token generation service
- [x] Implement active-session retrieval/creation logic
- [x] Enforce one with_doctor visit max
- [x] Implement queue ordering helper

## Stage 4 — Reception dashboard
- [x] Build reception dashboard shell
- [x] Add new-patient-to-queue form
- [x] Add existing-patient-to-queue flow
- [x] Add queue list partial
- [x] Add actions: urgent, cancel, requeue

## Stage 5 — Doctor dashboard
- [x] Build doctor dashboard shell
- [x] Add current patient card partial
- [x] Add next patients list partial
- [x] Add call-next action
- [x] Add done action
- [x] Add skip action
- [x] Add quick patient history panel

## Stage 6 — Display and settings
- [x] Build public display page
- [x] Add display partial refresh
- [x] Create settings page
- [x] Add clinic name and privacy toggles
- [x] Add daily reset behavior

## Stage 7 — PWA + deploy
- [x] Add manifest
- [x] Add icons placeholders
- [x] Add service worker shell
- [x] Ensure installable metadata
- [x] Finalize Docker deployment
- [x] Finalize Caddy routing

## Stage 8 — QA and hardening
- [x] Add test coverage for queue rules
- [x] Run functional smoke tests
- [x] Verify mobile layouts
- [x] Verify production static/media
- [x] Add backup script
