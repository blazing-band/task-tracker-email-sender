from email_sender.settings import SMTPSettings


class EmailService:
    def __init__(self, smtp_settings: SMTPSettings) -> None:
        self.smtp_settings = smtp_settings
