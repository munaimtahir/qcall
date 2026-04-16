# TESTS.md

## Testing layers
1. Model/unit tests
2. Service/business-rule tests
3. View permission tests
4. HTMX interaction tests
5. Smoke tests for critical workflows

## Must-pass acceptance tests
### Patient registry
- Create new patient
- Search patient by mobile number
- Search patient by MR number
- Prevent duplicate MR number when present

### Queue logic
- Create active daily queue session
- Issue sequential token numbers
- Prevent token duplication within session
- Ensure only one active with_doctor visit at a time
- Urgent patient ordering follows setting
- Skipped patient can be requeued

### Workflow
- Reception adds new patient to queue
- Reception adds existing patient to queue
- Doctor calls next patient
- Doctor marks current patient done
- Doctor skips current/waiting patient
- Cancelled/no-show patients remain in history

### Access control
- Reception cannot access admin-only settings actions unless permitted
- Doctor cannot perform unrelated admin actions
- Public display has no privileged controls

### PWA/deployment sanity
- Manifest resolves
- Static assets load
- Basic install metadata present
- App serves behind Caddy without broken static paths

## Suggested tools
- Django TestCase / pytest-django
- Factory Boy optional
- Coverage
- Playwright optional later for browser smoke flow
