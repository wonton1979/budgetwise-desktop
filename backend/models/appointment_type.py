from enum import Enum


class AppointmentType(str,Enum):
    IN_PERSON = 'in person'
    ONLINE = 'online'