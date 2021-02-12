#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages

# python namespace subpackage
# this namespace package follows PEP420
# https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

NAMESPACE_PACKAGE_NAME = "evaluation_tools"
SUBPACKAGE_NAME = "nwis_client"

# Namespace subpackage slug.
# Ex: mypkg.a # Where the namespace pkg = `mypkg` and the subpackage = `a`
SUBPACKAGE_SLUG = f"{NAMESPACE_PACKAGE_NAME}.{SUBPACKAGE_NAME}"

# Subpackage version
VERSION = "1.1.0"

# Package author information
AUTHOR = "Austin Raney"
AUTHOR_EMAIL = "arthur.raney@noaa.gov"

# Short sub-package description
DESCRIPTION = ""

# Package dependency requirements
REQUIREMENTS = [
    "pandas",
    "numpy",
    "requests",
    "requests-cache",
    "evaluation_tools._restclient@ git+https://github.com/NOAA-OWP/evaluation_tools.git@v1.3.0#subdirectory=python/_restclient",
]

setup(
    name=SUBPACKAGE_SLUG,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        "Private :: Do Not Upload to pypi server",
    ],
    description=DESCRIPTION,
    namespace_packages=[NAMESPACE_PACKAGE_NAME],
    packages=find_namespace_packages(include=[f"{NAMESPACE_PACKAGE_NAME}.*"]),
    install_requires=REQUIREMENTS,
)
