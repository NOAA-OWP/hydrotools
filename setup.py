#!/usr/bin/env python3
import subprocess
import sys
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

from typing import Dict, List
from pathlib import Path

# python root namespace package
# this namespace package follows PEP420
# https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

# This namespace package structure and configuration follows a pattern
# presented here:
# https://medium.com/@jherreras/python-microlibs-5be9461ad979

NAMESPACE_PACKAGE_NAME = "hydrotools"
SRC_ROOT = "python"

# Package author information
AUTHOR = "Jason Regina"
AUTHOR_EMAIL = "jason.regina@noaa.gov"
MAINTAINER = "Austin Raney"
MAINTAINER_EMAIL = "arthur.raney@noaa.gov"

# Namespace package version
VERSION = "2.0.0-alpha.0"
URL = "https://github.com/NOAA-OWP/hydrotools"

# Short sub-package description
DESCRIPTION = (
    "Suite of tools for retrieving USGS NWIS observations and evaluating "
    "National Water Model (NWM) data."
)

# Read information from relevant package files
LONG_DESCRIPTION = Path("README.md").read_text()
LICENSE = Path("LICENSE").read_text()

# Development requirements
DEVELOPMENT_REQUIREMENTS = ["pytest"]


def get_subpackage_names() -> List[str]:
    # This assumes that each subpackage has a setup.py and is located under python/
    root_dir = Path(__file__).resolve().parent
    path_to_subpackages = list(root_dir.glob("{}/*/setup.py".format(SRC_ROOT)))

    # Empty list. No subpackages found, may want to raise an exception here given the
    # context
    if not path_to_subpackages:
        return path_to_subpackages

    # Assumes directory structure `python/{{ sub-package name }}/setup.py`
    return [subpackage.parts[-2] for subpackage in path_to_subpackages]


def get_subpackage_slugs(subpackage_names: List[str]) -> List[str]:
    return [
        "{}.{}".format(NAMESPACE_PACKAGE_NAME, subpackage)
        for subpackage in subpackage_names
    ]


def build_subpackage_requirements() -> List[str]:
    subpackage_names = get_subpackage_names()
    subpackage_slugs = get_subpackage_slugs(subpackage_names)

    requirements = []
    for idx, slug in enumerate(subpackage_slugs):
        requirement_path = (
            "{slug}@ git+{URL}.git#subdirectory={SRC_ROOT}/{subpackage}".format(
                slug=slug, URL=URL, SRC_ROOT=SRC_ROOT, subpackage=subpackage_names[idx]
            )
        )
        requirements.append(requirement_path)

    return requirements


def build_subpackage_mapping() -> Dict[str, str]:
    subpackage_names = get_subpackage_names()

    subpackage_mapping = {}
    for name in subpackage_names:
        subpackage_mapping[name] = "{}/{}".format(SRC_ROOT, name)

    return subpackage_mapping


def install_subpackages(
    sources: dict,
) -> None:
    """Install all subpackages in a namespace package

    Parameters
    ----------
    sources : dict
        key: subpackage slug, value: subpackage relative location
    develop_flag : bool, optional
        Install in normal or development mode, by default normal
    """
    # absolute path
    ROOT_DIR = Path(__file__).resolve().parent
    for k, v in sources.items():
        try:
            subpackage_dir = str(ROOT_DIR / v)
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-e",
                    subpackage_dir,
                ]
            )
        except Exception as e:
            error_message = "An error occurred when installing %s" % (k,)
            raise Exception(error_message) from e


REQUIREMENTS = build_subpackage_requirements()
SUBPACKAGES = build_subpackage_mapping()

# Development installation
class Develop(develop):
    def run(self):
        install_subpackages(SUBPACKAGES)
        # Install development requirements
        for dev_requirement in DEVELOPMENT_REQUIREMENTS:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", dev_requirement]
            )


setup(
    name=NAMESPACE_PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    classifiers=[
        "Private :: Do Not Upload to pypi server",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    license=LICENSE,
    install_requires=REQUIREMENTS,
    extras_require={"test": DEVELOPMENT_REQUIREMENTS},
    python_requires=">=3.7",
    cmdclass={"develop": Develop},
)
