"""Step definitions for features/book_appointment.feature.

Each step is a thin adapter: it translates Gherkin phrases into calls on
booking.service.AppointmentService, so the scenarios stay the single
source of truth for the expected behaviour.
"""
import datetime as dt

from behave import given, when, then, register_type
import parse

from booking.service import AppointmentService


# Allows empty quoted values such as "" for a missing name.
@parse.with_pattern(r'[^"]*')
def parse_text(text):
    return text


register_type(Text=parse_text)


def _service(context):
    if not hasattr(context, "service"):
        context.service = AppointmentService(context.today, context.slots)
        for service, date, time in context.prebooked:
            context.service.book("Existing Resident", "LS1 1UR", service, date, time)
    return context.service


@given('today is "{today}"')
def step_today(context, today):
    context.today = dt.date.fromisoformat(today)


@given('the "{service}" service offers slots at "{times}"')
def step_slots(context, service, times):
    context.slots[service] = [t.strip() for t in times.split(",")]


@given('the "{time}" slot on "{date}" has already been booked')
def step_prebooked(context, time, date):
    context.prebooked.append(("Housing advice", date, time))


@when('"{name:Text}" with postcode "{postcode:Text}" requests a "{service:Text}" '
      'appointment on "{date:Text}" at "{time:Text}"')
def step_request(context, name, postcode, service, date, time):
    context.result = _service(context).book(name, postcode, service, date, time)


@then("the booking is {outcome}")
def step_outcome(context, outcome):
    assert outcome in ("confirmed", "not confirmed"), f"Unknown outcome: {outcome}"
    expected = outcome == "confirmed"
    assert context.result.confirmed == expected, (
        f'Expected booking to be {outcome} but service replied "{context.result.message}"')


@then('the booking reference starts with "{prefix}"')
def step_reference(context, prefix):
    assert context.result.reference.startswith(prefix), context.result.reference


@then('the "{time}" slot on "{date}" is no longer available')
def step_slot_taken(context, time, date):
    free = _service(context).available_slots("Housing advice", date)
    assert time not in free, f"{time} is still offered: {free}"


@then('the resident is told "{message}"')
def step_message(context, message):
    assert context.result.message == message, (
        f'Expected "{message}" but got "{context.result.message}"')


@then('the resident is offered the alternative slots "{times}"')
def step_alternatives(context, times):
    expected = [t.strip() for t in times.split(",")]
    assert context.result.alternatives == expected, context.result.alternatives
