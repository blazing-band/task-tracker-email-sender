import smtplib
from email.message import EmailMessage

from email_sender.enums import SmtpSecurity
from email_sender.settings import SMTPSettings


class EmailService:
    def __init__(self, smtp_settings: SMTPSettings) -> None:
        self.smtp_settings = smtp_settings

    def _create_smtp_session(self) -> smtplib.SMTP:
        if self.smtp_settings.smtp_security == SmtpSecurity.SSL:
            return smtplib.SMTP_SSL(self.smtp_settings.smtp_host, self.smtp_settings.smtp_port, timeout=30)

        smtp_session = smtplib.SMTP(self.smtp_settings.smtp_host, self.smtp_settings.smtp_port, timeout=30)
        smtp_session.starttls()
        return smtp_session

    def send_message(self, subject: str, body: str, destination_email: str) -> None:
        message = EmailMessage()
        message["From"] = self.smtp_settings.smtp_login
        message["To"] = destination_email
        message["Subject"] = subject
        message.set_content(body)

        with self._create_smtp_session() as smtp_session:
            smtp_session.login(self.smtp_settings.smtp_login, self.smtp_settings.smtp_password)
            smtp_session.send_message(message)
