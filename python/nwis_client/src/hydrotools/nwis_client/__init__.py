# removing __version__ import will cause build to fail. see: https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__

from .iv import IVDataService

import warnings

warnings.warn(
    "The hydrotools.nwis_client package is DEPRECATED. "
    "USGS will permanently decommssion the NWIS API in early 2027, "
    "which will break this library. Please migrate to hydrotools.waterdata_client",
    category=FutureWarning,
    stacklevel=2
)
