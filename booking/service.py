"""Appointment booking service for resident-facing council advice sessions."""
from dataclasses import dataclass, field
import itertools

from booking import validation
from booking.validation import ValidationError

SERVICE_CODES = {
    "Housing advice": "HA",
    "Council tax": "CT",
    "Resident support": "RS",
}


@dataclass
class BookingResult:
    confirmed: bool
    message: str
    reference: str = ""
    alternatives: list = field(default_factory=list)


@dataclass(frozen=True)
class Booking:
    reference: str
    name: str
    postcode: str
    service: str
    date: str
    time: str


class AppointmentService:
    """Books advice appointments against a set of published slots.

    `slots` maps a service name to the times it offers each weekday.
    `today` is injected so behaviour is repeatable in tests.
    """

    def __init__(self, today, slots):
        self.today = today
        self.slots = slots
        self.bookings = {}
        self._sequence = itertools.count(1)

    def _is_booked(self, service, date, time):
        return any((b.service, b.date, b.time) == (service, date, time)
                   for b in self.bookings.values())

    def available_slots(self, service, date):
        return [t for t in self.slots.get(service, [])
                if not self._is_booked(service, date, t)]

    def book(self, name, postcode, service, date, time):
        try:
            name = validation.validate_name(name)
            postcode = validation.validate_postcode(postcode)
            service = validation.validate_service(service, self.slots)
            date = validation.validate_date(date, self.today).isoformat()
            time = validation.validate_time(time, self.slots[service])
        except ValidationError as error:
            return BookingResult(False, str(error))

        if self._is_booked(service, date, time):
            return BookingResult(False, "That slot is no longer available",
                                 alternatives=self.available_slots(service, date))

        reference = f"{SERVICE_CODES.get(service, 'GEN')}-{next(self._sequence):04d}"
        self.bookings[reference] = Booking(reference, name, postcode, service, date, time)
        return BookingResult(True, "Your appointment is booked", reference)
