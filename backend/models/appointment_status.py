from enum import Enum


class AppointmentStatus(str,Enum):
    UPCOMING = 'upcoming'
    COMPLETED = 'completed'
    MISSED = 'missed'
    CANCELED = 'canceled'
    EXPIRED = 'expired'