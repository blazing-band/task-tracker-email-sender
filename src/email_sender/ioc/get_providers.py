from dishka import Provider

from .providers import (
    ServicesProvider,
    SettingsProvider,
)


def get_providers() -> list[Provider]:
    return [
        SettingsProvider(),
        ServicesProvider(),
    ]
