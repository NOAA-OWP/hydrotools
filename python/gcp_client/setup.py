#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages

# python namespace subpackage
# this namespace package follows PEP420
# https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

NAMESPACE_PACKAGE_NAME = "hydrotools"
SUBPACKAGE_NAME = "gcp_client"

# Namespace subpackage slug.
# Ex: mypkg.a # Where the namespace pkg = `mypkg` and the subpackage = `a`
SUBPACKAGE_SLUG = f"{NAMESPACE_PACKAGE_NAME}.{SUBPACKAGE_NAME}"

# Subpackage version
VERSION = "2.1.2"

# Package author information
AUTHOR = "Jason Regina"
AUTHOR_EMAIL = "jason.regina@noaa.gov"

# Short sub-package description
DESCRIPTION = "Retrieve National Water Model data from Google Cloud Platform."

# Package dependency requirements
REQUIREMENTS = ["pandas", "xarray", "google-cloud-storage", "h5netcdf", "tables", "numpy>=1.20.0"]

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
    package_data={
        "hydrotools.gcp_client": [
            "data/RouteLink_NWMv2.0.csv",
            "data/RouteLink_CONUS_NWMv2.1.6.csv",
            "data/RouteLink_HI.csv",
            "data/RouteLink_PuertoRico_NWMv2.1_20191204.csv",
        ]
    },
    install_requires=REQUIREMENTS,
)
