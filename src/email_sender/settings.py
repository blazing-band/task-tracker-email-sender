import os
from dataclasses import dataclass

from email_sender.enums.smtp_security import SmtpSecurity


@dataclass(frozen=True, slots=True, kw_only=True)
class SMTPSettings:
    smtp_host: str
    smtp_port: int
    smtp_login: str
    smtp_password: str
    smtp_security: SmtpSecurity


@dataclass(frozen=True, slots=True, kw_only=True)
class RabbitmqSettings:
    rabbit_host: str
    rabbit_port: int
    rabbit_username: str
    rabbit_password: str
    rabbit_virtual_host: str

    @property
    def url(self) -> str:
        return (
            f"amqp://{self.rabbit_username}:{self.rabbit_password}"
            f"@{self.rabbit_host}:{self.rabbit_port}/{self.rabbit_virtual_host}"
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class Settings:
    smtp: SMTPSettings
    rabbitmq: RabbitmqSettings


def load_settings() -> Settings:
    return Settings(
        smtp=SMTPSettings(
            smtp_host=os.environ["SMTP_HOST"],
            smtp_port=int(os.environ["SMTP_PORT"]),
            smtp_login=os.environ["SMTP_LOGIN"],
            smtp_password=os.environ["SMTP_PASSWORD"],
            smtp_security=SmtpSecurity(os.environ["SMTP_SECURITY"].lower()),
        ),
        rabbitmq=RabbitmqSettings(
            rabbit_host=os.environ["RABBITMQ_HOST"],
            rabbit_port=int(os.environ["RABBITMQ_PORT"]),
            rabbit_username=os.environ["RABBITMQ_USER"],
            rabbit_password=os.environ["RABBITMQ_PASS"],
            rabbit_virtual_host=os.environ["RABBITMQ_VHOST"],
        ),
    )
