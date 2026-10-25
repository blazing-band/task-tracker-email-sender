from typing import Any

from celery import Celery
from celery.signals import worker_shutdown
from dishka.integrations.celery import FromDishka, inject, setup_dishka
from kombu import Exchange, Queue

from email_sender.enums import RabbitMqExchange, RabbitMqQueues
from email_sender.ioc import get_sync_container
from email_sender.services import EmailService
from email_sender.settings import Settings

container = get_sync_container()


celery_app = Celery("tasks", broker=container.get(Settings).rabbitmq.url)
celery_app.conf.task_acks_late = True
celery_app.conf.task_reject_on_worker_lost = True
# RabbitMQ 4.x forbids transient non-exclusive queues
celery_app.conf.control_queue_exclusive = True
celery_app.conf.event_queue_exclusive = True

email_exchange = Exchange(RabbitMqExchange.EMAIL, type="direct", durable=True)

celery_app.conf.task_queues = (
    Queue(
        RabbitMqQueues.REGISTRATION_EMAIL,
        RabbitMqExchange.EMAIL,
        routing_key=RabbitMqQueues.REGISTRATION_EMAIL,
        durable=True,
    ),
)

celery_app.conf.task_routes = {
    "email_sender.send_user_registered_email": {
        "queue": RabbitMqQueues.REGISTRATION_EMAIL,
        "exchange": RabbitMqExchange.EMAIL,
        "routing_key": RabbitMqQueues.REGISTRATION_EMAIL,
    },
}

setup_dishka(container, celery_app)


@worker_shutdown.connect
def close_container(**kwargs: Any) -> None:
    container.close()


@celery_app.task(name="email_sender.send_user_registered_email")
@inject
def send_user_registered_email(
    email: str,
    subject: str,
    message: str,
    email_service: FromDishka[EmailService],
) -> None:
    email_service.send_message(
        subject=subject,
        body=message,
        destination_email=email,
    )
