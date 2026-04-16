# Plain-Language Application Description

## Product name
Queue Management MVP

## What it is
A clinic workflow application for a **single-doctor OPD**. It manages walk-in patients from reception to doctor consultation using a digital queue. It also keeps a lightweight history for returning patients so staff can identify whether a patient is new or previously seen.

## Main users
1. Reception
2. Doctor
3. Public display screen
4. Admin (basic settings only)

## Main purpose
Replace ad-hoc/manual patient turn handling with a simple digital queue that is easy to use in real life.

## What the application must do
- Register new or returning patients into the queue
- Search patients by mobile number or MR number
- Assign a token number for the current day
- Track queue status: waiting, with doctor, completed, skipped, cancelled, no-show
- Let the doctor call the next patient with one action
- Preserve lightweight visit history per patient
- Show a public queue display screen
- Reset queue logic safely each day while preserving historical records

## What is intentionally excluded from MVP
- Appointments
- Multi-doctor handling
- Billing
- Lab/pharmacy integration
- Full EMR
- Messaging automation
- Advanced analytics

## Product philosophy
This is not a hospital system. It is a focused OPD operational tool. Simplicity and speed matter more than feature count.
