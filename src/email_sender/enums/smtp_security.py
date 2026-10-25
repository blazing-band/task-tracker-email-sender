from enum import StrEnum


class SmtpSecurity(StrEnum):
    SSL = "ssl"
    STARTTLS = "starttls"
    NONE = "none"
