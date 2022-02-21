from logging import Filter
from typing import TYPE_CHECKING, Optional, Type
from uuid import uuid4
from ctlogging.context import correlation_id

if TYPE_CHECKING:
    from logging import LogRecord


class CorrelationId(Filter):
    def filter(self, record: 'LogRecord') -> bool:
        """
        Attach a correlation ID to the log record.

        Since the correlation ID is defined in the middleware layer, any
        log generated from a request after this point can easily be searched
        for, if the correlation ID is added to the message, or included as
        metadata.
        """
        cid = correlation_id.get()
        record.correlation_id = cid  # type: ignore[attr-defined]
        return True

