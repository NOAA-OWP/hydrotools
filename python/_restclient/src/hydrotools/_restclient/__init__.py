# removing __version__ import will cause build to fail. see: https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__

from ._restclient import RestClient
from .utilities import Alias, AliasGroup
from .urllib import Url, Variadic
from .urllib_types import Quote
from .async_client import ClientSession
