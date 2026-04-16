# QA_CHECKLIST.md

## Functional QA
- Can reception create a patient quickly?
- Can reception find returning patients reliably?
- Does adding a patient always assign the correct next token?
- Does the doctor dashboard always show a single current patient?
- Does call-next respect queue ordering?
- Does done/skip/cancel update all relevant screens?
- Does public display show correct token information?
- Does patient history preserve prior visits?

## UI QA
- Mobile-friendly reception workflow
- Large readable doctor current-patient card
- High-contrast display screen
- Clear status badges
- Search results easy to select

## Security QA
- Unauthorized users blocked from restricted pages
- Public display cannot mutate state
- CSRF working on forms/actions

## Operational QA
- Daily queue reset does not delete history
- Database backup can run successfully
- Docker containers restart cleanly
- Static files load in production
