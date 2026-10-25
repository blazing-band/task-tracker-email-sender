from fastapi import APIRouter, Response
from pydantic import BaseModel

from email_sender.tasks import send_email as send_email_task


class SendEmailRequest(BaseModel):
    name: str
    email: str


def get_send_email_router() -> APIRouter:
    router = APIRouter()

    @router.post("/send-email")
    async def send_email(request: SendEmailRequest) -> Response:
        send_email_task.delay(request.model_dump())
        return Response(status_code=202)

    return router
