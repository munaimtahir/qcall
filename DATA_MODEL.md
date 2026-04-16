# DATA_MODEL.md

## Patient
- id (UUID or big integer)
- mr_number (nullable initially, unique when present)
- full_name
- mobile_number
- age
- gender
- address (optional)
- notes (optional)
- created_at
- updated_at

## User
- id
- username
- full_name
- role: admin | reception | doctor
- is_active
- created_at
- updated_at

## DailyQueueSession
Represents one active day/session of the queue.
- id
- queue_date
- is_active
- start_token_number
- last_issued_token_number
- current_visit_id (nullable)
- created_at
- updated_at

Constraints:
- At most one active queue session per date.

## Visit
Represents one attendance of one patient on one day.
- id
- patient_id (FK)
- queue_session_id (FK)
- token_number
- status
- priority_level
- short_note
- doctor_note (optional)
- called_at (nullable)
- completed_at (nullable)
- created_by_id (FK user)
- created_at
- updated_at

Status enum:
- waiting
- with_doctor
- completed
- skipped
- cancelled
- no_show

Priority enum:
- normal
- urgent

Constraints:
- token_number unique within queue_session_id
- only one Visit may be status=with_doctor within an active session

## AppSetting
Simple key/value or structured settings table.
Suggested fields:
- id
- clinic_name
- queue_prefix (optional)
- public_display_show_patient_name (boolean)
- urgent_cases_jump_queue (boolean)
- daily_reset_mode
- created_at
- updated_at

## Queue rules
1. Tokens reset per daily queue session.
2. Only one patient can be in with_doctor at a time.
3. Urgent patients can move ahead of normal waiting patients but not replace the current patient.
4. Skipped patients can optionally be returned to waiting later.
5. Historical visits are never deleted during daily reset.
