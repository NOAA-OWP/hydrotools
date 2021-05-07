#!/usr/bin/env python3
import forge
import aiohttp
from typing import Dict, List, Union

# RestClient signature decorators

_PARAM_HEADER_KWOS = forge.insert(
    [
        forge.kwo("parameters", default={}, type=Dict[str, Union[str, List[str]]]),
        forge.kwo("headers", default={}, type=Dict[str, str]),
    ],
    before=lambda arg: arg.kind == forge.FParameter.VAR_KEYWORD,
)

GET_SIGNATURE = forge.compose(
    forge.copy(aiohttp.ClientSession.get),
    forge.returns(aiohttp.ClientResponse),
    _PARAM_HEADER_KWOS,
)

MGET_SIGNATURE = forge.compose(
    forge.copy(aiohttp.ClientSession.get, exclude="url"),
    forge.returns(List[aiohttp.ClientResponse]),
    forge.insert(
        forge.pok("urls", type=forge.fsignature(aiohttp.ClientSession.get)["url"].type),
        index=1,
    ),
    _PARAM_HEADER_KWOS,
)
