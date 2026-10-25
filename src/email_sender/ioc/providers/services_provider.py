from dishka import Provider, Scope, provide

from email_sender.services import EmailService


class ServicesProvider(Provider):
    # Scope.APP — один экземпляр на весь процесс worker'а, а не новый на каждую задачу.
    email_service = provide(EmailService, scope=Scope.APP)
