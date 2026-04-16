# TASKS.md

## Stage 0 — Foundation
- [ ] Initialize Django project structure
- [ ] Add apps: accounts, patients, queue, visits, display, settings_app
- [ ] Configure PostgreSQL connection
- [ ] Add settings split for dev/prod
- [ ] Add Tailwind integration
- [ ] Add Dockerfile and docker-compose.yml
- [ ] Add Caddy sample config

## Stage 1 — Auth and roles
- [ ] Implement login/logout
- [ ] Create role model or role field
- [ ] Seed admin, reception, doctor users
- [ ] Protect routes by role

## Stage 2 — Patients
- [ ] Create Patient model
- [ ] Add patient admin
- [ ] Create patient list/search page
- [ ] Create patient create/edit/detail pages
- [ ] Implement HTMX search partial

## Stage 3 — Queue core
- [ ] Create DailyQueueSession model
- [ ] Create Visit model
- [ ] Implement token generation service
- [ ] Implement active-session retrieval/creation logic
- [ ] Enforce one with_doctor visit max
- [ ] Implement queue ordering helper

## Stage 4 — Reception dashboard
- [ ] Build reception dashboard shell
- [ ] Add new-patient-to-queue form
- [ ] Add existing-patient-to-queue flow
- [ ] Add queue list partial
- [ ] Add actions: urgent, cancel, requeue

## Stage 5 — Doctor dashboard
- [ ] Build doctor dashboard shell
- [ ] Add current patient card partial
- [ ] Add next patients list partial
- [ ] Add call-next action
- [ ] Add done action
- [ ] Add skip action
- [ ] Add quick patient history panel

## Stage 6 — Display and settings
- [ ] Build public display page
- [ ] Add display partial refresh
- [ ] Create settings page
- [ ] Add clinic name and privacy toggles
- [ ] Add daily reset behavior

## Stage 7 — PWA + deploy
- [ ] Add manifest
- [ ] Add icons placeholders
- [ ] Add service worker shell
- [ ] Ensure installable metadata
- [ ] Finalize Docker deployment
- [ ] Finalize Caddy routing

## Stage 8 — QA and hardening
- [ ] Add test coverage for queue rules
- [ ] Run functional smoke tests
- [ ] Verify mobile layouts
- [ ] Verify production static/media
- [ ] Add backup script
