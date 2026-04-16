# AGENT.md

## Role
You are the sole implementation agent for this repository. Work in large, coherent phases rather than overly small edits.

## Mission
Build a production-lean MVP for a **single-doctor OPD queue management web application** using Django, PostgreSQL, Django templates, HTMX, and Tailwind CSS.

## Guardrails
- Do not change the locked stack.
- Do not introduce React, Vue, Next.js, Supabase, or native Android as primary implementation paths.
- Do not add appointments in MVP.
- Do not add multi-doctor logic in MVP.
- Do not overengineer real-time sync initially; use HTMX-triggered partial refresh and short interval refresh where suitable.
- Keep the app monolithic.
- Prefer explicit, readable business logic over abstraction-heavy patterns.
- Preserve auditability of queue transitions.
- Privacy-first public display: token-first, patient-name display behind explicit setting.

## Working method
1. Read all docs in this pack first.
2. Implement by stage in ROADMAP.md and TASKS.md.
3. After each stage, run tests and update status.
4. Keep docs aligned with actual code.
5. Produce evidence of completion for each stage.

## Output discipline
- Do not silently change product scope.
- If a gap is found, document it and resolve it in the smallest coherent way.
- Use TODO markers sparingly; prefer complete implementation.
