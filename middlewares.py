import logging

import sentry_sdk
from fastapi import Request
from sentry_sdk.integrations.logging import LoggingIntegration
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class SentryMiddleware(BaseHTTPMiddleware):
    def __init__(self, app=None, dns="", *args, **kwargs):
        super().__init__(app)
        sentry_logging = LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR,  # Send errors as events
        )
        kwargs["integrations"] = [sentry_logging]
        sentry_sdk.init(dns, kwargs)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            with sentry_sdk.push_scope() as scope:
                scope.set_context("request", request)
                user_id = "test_user_id"  # when available
                scope.user = {
                    "ip_address": request.client.host,
                    "id": user_id,
                    "name": "test_user",
                }
                sentry_sdk.capture_exception(e)
            raise e
