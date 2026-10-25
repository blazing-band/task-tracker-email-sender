from typing import Any

from celery import Celery
from celery.signals import worker_shutdown
from dishka.integrations.celery import FromDishka, inject, setup_dishka

from email_sender.ioc import get_sync_container
from email_sender.services import EmailService

broker_url = "amqp://rabbit:rabbit@localhost"
celery_app = Celery("tasks", broker=broker_url)
celery_app.conf.control_queue_exclusive = True

container = get_sync_container()
setup_dishka(container, celery_app)


@worker_shutdown.connect
def close_container(**kwargs: Any) -> None:
    container.close()


@celery_app.task
@inject
def send_email(
    payload: dict[str, Any],
    email_service: FromDishka[EmailService],
) -> None:
    # TODO get data from queue, form message and send email
    pass
