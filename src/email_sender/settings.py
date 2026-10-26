import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class AppSettings:
    cors_origins: list[str]


@dataclass(frozen=True, slots=True, kw_only=True)
class SMTPSettings:
    smtp_host: str
    smtp_port: int


@dataclass(frozen=True, slots=True, kw_only=True)
class RabbitmqSettings:
    rabbit_host: str
    rabbit_port: int
    rabbit_username: str
    rabbit_password: str
    rabbit_virtual_host: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Settings:
    # app: AppSettings
    smtp: SMTPSettings


def load_settings() -> Settings:
    return Settings(
        # app=AppSettings(cors_origins=os.environ["CORS_ORIGINS"].split(",")),
        smtp=SMTPSettings(
            smtp_host=os.environ["SMTP_HOST"],
            smtp_port=int(os.environ["SMTP_PORT"]),
        ),
    )
