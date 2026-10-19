"""Command-line demonstration of the resident appointment booking prototype.

Usage: python app.py "Amina Khan" "LS1 4AP" "Housing advice" 2026-11-05 10:00
"""
import datetime as dt
import sys

from booking.service import AppointmentService

PUBLISHED_SLOTS = {
    "Housing advice": ["09:00", "10:00", "11:00", "14:00", "15:00"],
    "Council tax": ["09:30", "10:30", "13:30"],
    "Resident support": ["10:00", "12:00", "15:00"],
}


def main(argv):
    if len(argv) != 5:
        print(__doc__.strip())
        return 2
    service = AppointmentService(dt.date.today(), PUBLISHED_SLOTS)
    result = service.book(*argv)
    print(result.message)
    if result.confirmed:
        print(f"Booking reference: {result.reference}")
    elif result.alternatives:
        print("Other times that day: " + ", ".join(result.alternatives))
    return 0 if result.confirmed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
