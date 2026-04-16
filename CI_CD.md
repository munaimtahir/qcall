# CI_CD.md

## Minimal CI pipeline
1. Install dependencies
2. Run formatting/lint checks
3. Run Django tests
4. Collect static in CI dry-run mode if configured
5. Build Docker image

## Recommended checks
- Python formatting: ruff format or black
- Lint: ruff
- Templates: optional html validator later
- Tests: pytest or Django test runner
- Security baseline: `python manage.py check --deploy` for production settings profile

## CD approach for MVP
Manual deploy is acceptable initially.

## Deployment steps
- Pull latest code
- Build/restart containers
- Run migrations
- Collect static
- Verify health pages and login

## Evidence to keep
- migration log
- test summary
- deployment checklist result
