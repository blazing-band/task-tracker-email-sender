from dishka import Provider, Scope, provide

from email_sender.settings import Settings, SMTPSettings, load_settings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return load_settings()

    @provide(scope=Scope.APP)
    def get_smtp_settings(self, settings: Settings) -> SMTPSettings:
        return settings.smtp
