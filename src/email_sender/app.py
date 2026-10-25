from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from email_sender.ioc import get_container
from email_sender.logger import set_up_logger
from email_sender.router import get_send_email_router
from email_sender.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    set_up_logger()
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:

    app = FastAPI(lifespan=lifespan)

    app.include_router(get_send_email_router())
    # app.add_exception_handler(
    #     exc_class_or_status_code=RequestValidationError,
    #     handler=custom_request_validation_error_handler,  # type: ignore[arg-type]
    # )
    # app.add_exception_handler(exc_class_or_status_code=Exception, handler=exception_handler)
    container = get_container()

    setup_dishka(container, app)

    settings = container.get_sync(Settings)

    app.add_middleware(
        CORSMiddleware,
        settings.app.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def main() -> None:
    uvicorn.run(app="email_sender.app:create_app", factory=True, port=8080, reload=True)


if __name__ == "__main__":
    main()
