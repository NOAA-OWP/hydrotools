#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages

# python namespace subpackage
# this namespace package follows PEP420
# https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

NAMESPACE_PACKAGE_NAME = "hydrotools"
SUBPACKAGE_NAME = "_restclient"

# Namespace subpackage slug.
# Ex: mypkg.a # Where the namespace pkg = `mypkg` and the subpackage = `a`
SUBPACKAGE_SLUG = f"{NAMESPACE_PACKAGE_NAME}.{SUBPACKAGE_NAME}"

# Subpackage version
VERSION = "3.0.0"

# Package author information
AUTHOR = "Austin Raney"
AUTHOR_EMAIL = "arthur.raney@noaa.gov"

# Short sub-package description
DESCRIPTION = "General REST api client with built in request caching and retries."

# Package dependency requirements
REQUIREMENTS = ["aiohttp", "aiohttp_client_cache", "python-forge", "aiosqlite"]
DEVELOPMENT_REQUIREMENTS = ["pytest", "pytest-aiohttp"]


setup(
    name=SUBPACKAGE_SLUG,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=[],
    description=DESCRIPTION,
    url="https://www.github.com/NOAA-OWP/hydrotools",
    license="USDOC",
    namespace_packages=[NAMESPACE_PACKAGE_NAME],
    packages=find_namespace_packages(include=[f"{NAMESPACE_PACKAGE_NAME}.*"]),
    install_requires=REQUIREMENTS,
    extras_require={"develop": DEVELOPMENT_REQUIREMENTS},
)
