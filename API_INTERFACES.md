# API_INTERFACES.md

This project is server-rendered first. Most interfaces are standard Django views. HTMX endpoints return HTML partials, not JSON, unless JSON is explicitly needed.

## Page routes
- `/login/`
- `/logout/`
- `/reception/`
- `/doctor/`
- `/patients/`
- `/patients/<id>/`
- `/display/`
- `/settings/`

## HTMX/action routes
### Patient search
- `GET /patients/search/`
  - params: `q`
  - returns: HTML partial list of matching patients

### Create patient and queue visit
- `POST /queue/add/`
  - form fields: patient inputs + optional short note + priority
  - creates patient if new and adds Visit to active queue session
  - returns: updated queue list partial + success state

### Add existing patient to queue
- `POST /queue/add-existing/`
  - fields: patient_id, priority, short_note
  - returns: updated queue list partial

### Call next
- `POST /queue/call-next/`
  - selects next eligible waiting visit
  - sets prior with_doctor visit to completed or requires explicit handling depending on UX choice
  - returns: current patient partial + queue partial + display partial trigger

### Mark done
- `POST /queue/<visit_id>/done/`
  - transitions with_doctor -> completed
  - returns updated dashboard partials

### Skip
- `POST /queue/<visit_id>/skip/`
  - transitions waiting/with_doctor -> skipped

### Cancel
- `POST /queue/<visit_id>/cancel/`
  - transitions waiting -> cancelled

### Requeue skipped patient
- `POST /queue/<visit_id>/requeue/`
  - transitions skipped -> waiting

### Mark urgent
- `POST /queue/<visit_id>/urgent/`
  - sets priority_level=urgent and reorders display/order if configured

### Refresh partials
- `GET /queue/partials/list/`
- `GET /queue/partials/current/`
- `GET /display/partials/panel/`

## Notes
- Use POST for all state-changing actions.
- Protect all actions with role checks.
- Prefer Django form validation for writes.
- Keep business rules inside services/domain helpers, not templates.
