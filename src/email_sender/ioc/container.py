from dishka import AsyncContainer, Container, make_async_container, make_container

from .get_providers import get_providers


def get_container() -> AsyncContainer:
    return make_async_container(*get_providers())


# Celery выполняет задачи синхронно, поэтому ему нужен обычный (не async) контейнер.
def get_sync_container() -> Container:
    return make_container(*get_providers())
