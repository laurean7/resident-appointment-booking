"""Appointment booking service for resident-facing council advice sessions."""
from dataclasses import dataclass, field
import datetime as dt
import itertools


@dataclass
class BookingResult:
    confirmed: bool
    message: str
    reference: str = ""
    alternatives: list = field(default_factory=list)


class AppointmentService:
    """Books advice appointments against a set of published slots."""

    def __init__(self, today, slots):
        self.today = today
        self.slots = slots
        self._booked = set()
        self._sequence = itertools.count(1)

    def available_slots(self, service, date):
        return [t for t in self.slots.get(service, [])
                if (service, date, t) not in self._booked]

    def book(self, name, postcode, service, date, time):
        self._booked.add((service, date, time))
        reference = f"HA-{next(self._sequence):04d}"
        return BookingResult(True, "Your appointment is booked", reference)
