# Resident Appointment Booking (SWE6301 prototype)

A small Python prototype for a local authority's resident-facing
appointment booking service, specified with Behaviour-Driven Development
(BDD) using Gherkin and `behave`.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
behave
```

To try the prototype by hand:

```bash
python app.py "Amina Khan" "LS1 4AP" "Housing advice" 2026-11-05 10:00
```

## Structure

| Path | Purpose |
| --- | --- |
| `features/book_appointment.feature` | User story, acceptance criteria and Gherkin scenarios |
| `features/steps/booking_steps.py` | Step definitions binding Gherkin to the service |
| `booking/service.py` | Booking rules: slots, double-booking, references |
| `booking/validation.py` | Resident-facing input validation |
| `app.py` | Command-line demo |
