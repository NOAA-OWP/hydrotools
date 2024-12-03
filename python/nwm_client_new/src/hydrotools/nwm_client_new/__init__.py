# removing __version__ import will cause build to fail. see: https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__

import warnings

warnings.warn(
    "nwm_client_new will be renamed to nwm_client for v8.0+. Update imports as necessary.",
    FutureWarning
    )
