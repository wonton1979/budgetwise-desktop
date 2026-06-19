from enum import Enum


class OnlinePlatform(str,Enum):
    ZOOM = 'zoom'
    MICROSOFT_TEAMS = 'microsoft teams'
    SLACK = 'slack'
    OTHER = 'other'
    GOOGLE_MEET='google meet'
