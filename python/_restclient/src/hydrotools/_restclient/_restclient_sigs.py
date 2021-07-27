import forge
import aiohttp
from typing import Dict, List, Union

# RestClient signature decorators

GET_SIGNATURE = forge.compose(
    forge.copy(aiohttp.ClientSession.get),
    forge.modify("url", default=None),
    forge.returns(aiohttp.ClientResponse),
    forge.insert(
        [
            forge.kwo("parameters", default={}, type=Dict[str, Union[str, List[str]]]),
            forge.kwo("headers", default={}, type=Dict[str, str]),
        ],
        before=lambda arg: arg.kind == forge.FParameter.VAR_KEYWORD,
    ),
)

MGET_SIGNATURE = forge.compose(
    forge.copy(aiohttp.ClientSession.get, exclude="url"),
    forge.returns(List[aiohttp.ClientResponse]),
    forge.insert(
        forge.pok(
            "urls",
            type=forge.fsignature(aiohttp.ClientSession.get)["url"].type,
            default=None,
        ),
        index=1,
    ),
    forge.insert(
        [
            forge.kwo(
                "parameters", default={}, type=List[Dict[str, Union[str, List[str]]]]
            ),
            forge.kwo("headers", default={}, type=List[Dict[str, str]]),
        ],
        before=lambda arg: arg.kind == forge.FParameter.VAR_KEYWORD,
    ),
)
