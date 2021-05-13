from aiohttp_client_cache import CachedSession
import asyncio
import forge
from functools import partial
from inspect import Parameter
from random import random
import warnings

__all__ = ["ClientSession"]

RETRY_STATUS_CODES = frozenset({503, 429, 301})


def forge_client_session(init):
    """ Forge CachedSession.__init__ method signature """
    forged_signature = forge.compose(
        forge.copy(CachedSession.__init__),
        forge.insert(
            [
                forge.kwarg("retry", default=True, type=bool),
                forge.kwarg("n_retries", default=3, type=int),
            ],
            before=lambda x: x.kind == Parameter.KEYWORD_ONLY,
        ),
    )(init)
    return forged_signature


with warnings.catch_warnings():
    # Ignore aiohttp.ClientSession Inheritance warning
    # This is the same approach that aiohttp_client_cache takes to implement their CachedSession object
    # As noted by aiohttp_client_cache in their implementation:
    # Since only _request() is overridden, there is minimal chance of breakage, but still possible
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, message="Inheritance class"
    )

    class ClientSession(CachedSession):
        @forge_client_session
        def __init__(self, *, retry: bool = True, n_retries: int = 3, **kwargs):

            self._retry = retry
            self._n_retries = n_retries
            super().__init__(**kwargs)

        @forge.copy(CachedSession._request)
        async def _request(self, *args, **kwargs):
            bound_resp = partial(super()._request, *args, **kwargs)
            resp = await bound_resp()

            if (
                self._retry is True
                and resp.status in RETRY_STATUS_CODES
                and self._n_retries > 0
            ):
                resp = await backoff(bound_resp, self._n_retries)

            return resp


async def backoff(request, n: int = 3):
    resp = None
    for nth in range(n):
        resp = await request()

        if nth == (n - 1):
            break  # break early on last iteration

        if resp.status not in RETRY_STATUS_CODES:
            break  # break, return resp
        # Exponential backoff
        sleep_length = (2 ** nth) + (random() / 10)
        await asyncio.sleep(sleep_length)

    return resp
