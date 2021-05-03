#!/usr/bin/env python3

import asyncio
from typing import Coroutine


__all__ = []


class AsyncToSerialHelper:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
    ) -> None:
        self._loop = loop

        # if loop not passed, get running or start new
        if loop is None:
            self._loop = asyncio.get_event_loop()

    def _add_to_loop(self, coro: Coroutine):
        return self._loop.run_until_complete(coro)
