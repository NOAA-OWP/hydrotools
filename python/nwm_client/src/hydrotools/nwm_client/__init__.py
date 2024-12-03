# removing __version__ import will cause build to fail. see: https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__
