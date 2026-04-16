# Final AI Developer Prompt

You are building a complete MVP for a **single-doctor OPD queue management web application**.

## Locked product scope
Build a system that allows:
- reception to register new patients and search returning patients
- assign daily token numbers
- manage a live queue
- let the doctor call next / mark done / skip
- preserve lightweight patient visit history
- show a public display screen

Appointments are excluded from MVP.
Multi-doctor support is excluded from MVP.
Billing and lab integration are excluded from MVP.

## Locked stack
- Backend: Django
- Database: PostgreSQL
- Frontend: Django templates + HTMX + Tailwind CSS
- JS: Alpine.js only where small local interactions help
- Deployment: Docker + Caddy
- PWA support required

## Architectural rules
- Build a Django monolith
- Do not create a separate SPA frontend
- Use server-rendered pages
- Use HTMX for partial updates and queue actions
- Keep business logic in Python services/helpers, not in templates
- Enforce role-based access control for admin / reception / doctor
- Public display must be read-only
- Keep the codebase simple, explicit, and maintainable

## Required Django apps
- accounts
- patients
- queue
- visits
- display
- settings_app

## Required core models
Implement models and constraints based on DATA_MODEL.md.

## Required workflows
1. Reception searches patient by mobile/MR number.
2. If patient exists, add to today’s queue.
3. If patient does not exist, create patient and add to queue.
4. Queue token is assigned sequentially within today’s active queue session.
5. Doctor dashboard shows current patient and next waiting patients.
6. Doctor can call next, mark done, and skip.
7. Visit is stored in patient history.
8. Public display updates with current token and next tokens.
9. Daily reset preserves history but starts a fresh active queue session.

## UX expectations
- Reception dashboard should prioritize speed and search
- Doctor dashboard should prioritize clarity and single-click actions
- Display screen should be high contrast and token-first
- Mobile responsiveness required

## Implementation phases
Follow ROADMAP.md and TASKS.md in order. Complete each stage coherently before moving to the next.

## Deliverables
- Working Django project scaffold
- Implemented models, migrations, views, templates, routes, and services
- HTMX partials for queue interactions
- Tailwind-based UI
- Basic tests for queue correctness and access control
- Docker + Caddy deployment files
- PWA manifest and installable shell
- Updated docs reflecting final implementation

## Quality bar
- Do not leave major TODOs where implementation is reasonable
- Run tests after each major stage
- Keep templates modular
- Keep naming consistent
- Avoid framework churn or unnecessary abstractions

## Final verification checklist
- patient search works
- patient creation works
- add-to-queue works
- token generation works
- call-next works
- done/skip/cancel works
- current patient uniqueness enforced
- patient history visible
- public display works
- PWA metadata present
- docker deployment works

Now implement the project end-to-end using this repository pack as the source of truth.
