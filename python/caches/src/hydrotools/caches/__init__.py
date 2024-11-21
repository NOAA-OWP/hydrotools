# removing __version__ import will cause build to fail. see: https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__

import warnings

warnings.warn(
    "hydrotools.caches is no longer supported. Use hydrotools.nwm_client_new.ParquetStore. https://pypi.org/project/hydrotools.nwm-client-new/",
    FutureWarning
    )
