import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from fedora_messaging import exceptions as fm_exceptions
from starlette.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_502_BAD_GATEWAY

from webhook_to_fedora_messaging.endpoints.models.message import MessageResult
from webhook_to_fedora_messaging.endpoints.util import return_service_from_uuid
from webhook_to_fedora_messaging.exceptions import SignatureMatchError
from webhook_to_fedora_messaging.models import Service
from webhook_to_fedora_messaging.publishing import publish

from .parser import parser


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/messages")


@router.post(
    "/{uuid}",
    status_code=HTTP_202_ACCEPTED,
    response_model=MessageResult,
    tags=["messages"],
)
async def create_message(
    body: dict,
    request: Request,
    service: Service = Depends(return_service_from_uuid),  # noqa : B008
):
    """
    Create a message with the requested attributes
    """
    try:
        message = await parser(service, request)
    except (SignatureMatchError, ValueError, KeyError) as expt:
        raise HTTPException(
            HTTP_400_BAD_REQUEST, f"Message could not be dispatched - {expt}"
        ) from expt

    try:
        await publish(message)
    except (fm_exceptions.ConnectionException, fm_exceptions.PublishException) as expt:
        logger.exception(
            "Could not send message %s for service %s (%s)", message.id, service.name, service.id
        )
        raise HTTPException(HTTP_502_BAD_GATEWAY, f"Message could not be sent: {expt}") from expt
    service.sent += 1
    return {"data": {"message_id": message.id}}
