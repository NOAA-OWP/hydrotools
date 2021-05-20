#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages
from pathlib import Path

# python namespace subpackage
# this namespace package follows PEP420
# https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

NAMESPACE_PACKAGE_NAME = "hydrotools"
SUBPACKAGE_NAME = "caches"

# Namespace subpackage slug.
# Ex: mypkg.a # Where the namespace pkg = `mypkg` and the subpackage = `a`
SUBPACKAGE_SLUG = f"{NAMESPACE_PACKAGE_NAME}.{SUBPACKAGE_NAME}"

# Subpackage version
VERSION = "0.1.1"

# Package author information
AUTHOR = "Jason Regina"
AUTHOR_EMAIL = "jason.regina@noaa.gov"

# Short sub-package description
DESCRIPTION = "Variety of object caching utilities for HydroTools."

# Long description
with (Path(__file__).parent / "README.md").open('r') as f:
    LONG_DESCRIPTION = f.read()

# Package dependency requirements
REQUIREMENTS = [
    "pandas",
    "tables"
]

setup(
    name=SUBPACKAGE_SLUG,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: Free To Use But Restricted",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Hydrology"
    ],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://www.github.com/NOAA-OWP/hydrotools",
    license="USDOC",
    namespace_packages=[NAMESPACE_PACKAGE_NAME],
    packages=find_namespace_packages(include=[f"{NAMESPACE_PACKAGE_NAME}.*"]),
    install_requires=REQUIREMENTS,
)
