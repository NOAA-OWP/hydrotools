# removing __version__ import will cause build to fail. see: https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__

from . import http

try:
    from . import gcp
except ImportError as e:
    # google-cloud-storage not installed
    if "google-cloud-storage" in e.msg:
        pass
    else:
        raise e

import warnings

warnings.warn(
    "nwm_client is no longer supported. Use https://pypi.org/project/hydrotools.nwm-client-new/",
    FutureWarning
    )
