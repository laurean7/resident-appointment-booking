"""Appointment booking service for resident-facing council advice sessions."""


class AppointmentService:
    """Books advice appointments against a set of published slots."""

    def __init__(self, today, slots):
        self.today = today
        self.slots = slots

    def book(self, name, postcode, service, date, time):
        raise NotImplementedError("Booking is not implemented yet")
