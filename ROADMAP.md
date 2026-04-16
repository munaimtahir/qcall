# Multi-Stage Development Roadmap

## Stage 0 — Project foundation
- Create Django project and apps
- Configure PostgreSQL
- Add environment settings split (base/dev/prod)
- Set up Tailwind build flow
- Prepare Docker and Caddy templates
- Add auth and role model foundations

## Stage 1 — Patient registry foundation
- Patient model and admin
- Search by mobile number and MR number
- Patient create/edit/detail pages
- Returning-patient lookup flow

## Stage 2 — Queue engine MVP
- Daily queue session model
- Visit model
- Token generation logic
- Queue ordering rules
- Reception dashboard
- Add patient to today’s queue
- Queue list with status badges

## Stage 3 — Doctor workflow
- Doctor dashboard
- Current patient card
- Next-patient list
- Call next / done / skip actions
- Quick patient history panel

## Stage 4 — Public display and settings
- Public display screen
- Auto-refresh queue panel
- Settings page for clinic name, token format, privacy flags, queue reset rules
- Daily reset safeguards

## Stage 5 — PWA + deployment
- Manifest
- Icons
- Basic service worker shell
- Mobile install behavior
- Docker deployment and Caddy reverse proxy

## Stage 6 — Stabilization and hardening
- Test edge cases
- Role enforcement
- Data validation
- Backup script
- Smoke tests and operational checklist

## Deferred after MVP
- Multi-doctor queue
- Appointments
- SMS/WhatsApp alerts
- Billing linkage
- Rich longitudinal patient chart
