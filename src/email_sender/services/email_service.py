import smtplib

from email_sender.settings import SMTPSettings


class EmailService:
    def __init__(self, smtp_settings: SMTPSettings) -> None:
        self.smtp_session: smtplib.SMTP = smtplib.SMTP(smtp_settings.smtp_host, smtp_settings.smtp_port)

    # def _create_smtp_session(self, smtp_settings: SMTPSettings) -> smtplib.SMTP:

    def send_message(self, message: str, destination_email: str):
        self.smtp_session.sendmail(from_addr="TEST_SMTP", to_addrs=destination_email, msg=message)

