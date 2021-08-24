import asyncio
from typing import Callable, Coroutine
from functools import partial, wraps


__all__ = []


class AsyncToSerialHelper:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
    ) -> None:
        self._loop = loop  # type: asyncio.AbstractEventLoop

        # if loop not passed, get running or start new
        if loop is None:
            self._loop = asyncio.get_event_loop()

    def _add_to_loop(self, coro: Coroutine):
        """ Add coro to event loop via run_until_complete """
        try:
            return self._loop.run_until_complete(coro)

        except RuntimeError as e:
            try:
                # `RuntimeError: This event loop is already running` thrown by jupyter notebook
                # See hydrotools #99 for context and notebook #3397 for detail
                import nest_asyncio

                nest_asyncio.apply()

                return self._loop.run_until_complete(coro)
            except ModuleNotFoundError:
                error_message = (
                    "nest_asycnio package not found. Install using `pip install nest_asycnio`.\n"
                    "See https://github.com/NOAA-OWP/hydrotools/issues/99 for more detail."
                )
                raise ModuleNotFoundError(error_message) from e

    def _wrap_func_in_coro(self, func: Callable, *args, **kwargs):
        """ Create partial func; wrap and call partial in coro; return coro """
        part = partial(func, *args, **kwargs)

        async def wrap():
            return part()

        return wrap

    def _wrap_coro_in_callable(self, coro: Coroutine) -> Callable:
        """ Wrap coro in method (that accepts args, kwargs) which adds coro to event loop. """

        @wraps(coro)
        def wrap(*args, **kwargs):
            return self._add_to_loop(coro(*args, **kwargs))

        return wrap
