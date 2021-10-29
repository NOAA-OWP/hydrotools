# removing __version__ import will cause build to fail. see: https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__

from .gcp import NWMDataService
import warnings

warning_message = "Importing gcp_client is deprecated. Import hydrotools.nwm_client.gcp"
warnings.warn(warning_message, UserWarning)
