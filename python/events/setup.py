#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages

# python namespace subpackage
# this namespace package follows PEP420
# https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

NAMESPACE_PACKAGE_NAME = "evaluation_tools"
SUBPACKAGE_NAME = "events"

# Namespace subpackage slug.
# Ex: mypkg.a # Where the namespace pkg = `mypkg` and the subpackage = `a`
SUBPACKAGE_SLUG = f"{NAMESPACE_PACKAGE_NAME}.{SUBPACKAGE_NAME}"

# Subpackage version
VERSION = "0.2.2"

# Package author information
AUTHOR = "Jason Regina"
AUTHOR_EMAIL = "jason.regina@noaa.gov"

# Short sub-package description
DESCRIPTION = "Various methods to support event-based evaluations."

# Package dependency requirements
REQUIREMENTS = [
    "pandas",
]

setup(
    name=SUBPACKAGE_SLUG,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        "",
    ],
    description=DESCRIPTION,
    namespace_packages=[NAMESPACE_PACKAGE_NAME],
    packages=find_namespace_packages(include=[f"{NAMESPACE_PACKAGE_NAME}.*"]),
    package_data={},
    install_requires=REQUIREMENTS,
)
