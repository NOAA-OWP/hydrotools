# Guidance on how to contribute

There are two primary ways to help:

- Using the issue tracker, and
- Changing the code-base.

## Using the issue tracker

Use the issue tracker to suggest feature requests, report bugs, and ask questions.
This is also a great way to connect with the developers of the project as well
as others who are interested in this solution.

Use the issue tracker to find ways to contribute. Find a bug or a feature, mention in
the issue that you will take on that effort, then follow the _Changing the code-base_
guidance below.

## Changing the code-base

Generally speaking, you should fork this repository, make changes in your
own fork, and then submit a pull request. All new code should have associated
unit tests that validate implemented features and the presence or lack of defects.
Additionally, the code should follow any stylistic and architectural guidelines
prescribed by the project.

## Contribution Guidelines

### Setting Up Development Environment

In general, we suggest contributors fork the repository, create a new branch,
and submit a PR. This consists of three main steps:

- Fork, Clone, and Branch (`git` related things)
- Setup development and develop
- Open a pull request

#### Fork, Clone, and Branch

1. Fork repository. This creates a copy for yourself under your username and is done on GitHub.

2. Clone your fork. Make a local copy of your fork

```bash
git clone git@github.com:{{ user.name }}/hydrotools.git && cd hydrotools
```

3. Create a new branch. Open a new branch off of `master` for which you will work

```bash
git checkout -b new_feature_branch
```

#### Setup development and develop

1. Setup and activate virtual environment.

```bash
# Create virtual environment
python -m venv env
# Activate virtual environement
./env/bin/activate
```

2. Install development version of package

NOTE: `pip install -e .` will not work if install entire namespace package. Use the following:

```bash
python setup.py develop
```

3. Develop


#### Open A Pull Request

Once you are done/ready to start the pull request process!

### Pull Request Guidelines

Before you submit a pull request, please verify that you meet the guidelines
outlined in [`PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).
Additionally, the following guidelines should also be met:

1. If the pull request introduces code or changes to existing code, tests
should be included. This project supports the usage of both `pytest` and
`unittest`.
2. Pull requests must pass all GitHub Actions CI test.
3. Usage of non-standard python packages should be kept to a minimum.

### Coding Standards

- [Black](https://pypi.org/project/black/)
- `pytest` or `unittest` for testing
- New _tools_ should be added as [subpackages](#adding-new-subpackages)

### Adding New Subpackages

This project uses python native `namespace` packaging as outlined introduced in [PEP 420](https://www.python.org/dev/peps/pep-0420/). This allows all or just pieces of the package be installed by a user. To maintain this functionality the following guidelines must be followed:

1. New subpackages should be added under the `/python` in a directory with their given name. Example: `nwis_client`.
2. The structure of the subpackage should look as follows:

```bash
python
└── my_subpackage/
    ├── src/
    │   └── hydrotools/
    │       └── my_subpackage/
    │           ├── __init__.py
    │           ├── foo.py
    │           └── _version.py
    ├── tests/
    ├── CONTRIBUTION.md -> ../../CONTRIBUTION.md
    ├── LICENSE -> ../../LICENSE
    ├── SECURITY.md -> ../../SECURITY.md
    ├── TERMS.md -> ../../TERMS.md
    ├── README.md
    ├── pyproject.toml
    ├── pytest.ini -> ../../pytest.ini
    └── setup.cfg
```

3. The package's `setup.cfg` should use the following template:

```ini
[metadata]
name = hydrotools.{{ SUBPACKAGE_NAME }}
version = attr: hydrotools.{{ SUBPACKAGE_NAME }}._version.__version__
author = {{ AUTHOR }}
author_email = {{ AUTHOR_EMAIL }}
description = {{ SHORT_DESCRIPTION }}
long_description = file: README.md
long_description_content_type = text/markdown; charset=UTF-8
license = USDOC
license_files =
    LICENSE
url = https://github.com/NOAA-OWP/hydrotools
project_urls =
    Documentation = https://noaa-owp.github.io/hydrotools/hydrotools.{{ SUBPACKAGE_NAME }}.html
    Source = https://github.com/NOAA-OWP/hydrotools/tree/main/python/nwm_client
    Tracker = https://github.com/NOAA-OWP/hydrotools/issues
classifiers =
    Development Status :: 3 - Alpha
    Intended Audience :: Education
    Intended Audience :: Science/Research
    License :: Free To Use But Restricted
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    Topic :: Scientific/Engineering :: Hydrology
    Operating System :: OS Independent

[options]
packages = find_namespace:
package_dir =
    =src
install_requires =
  {{ PACKAGE_REQUIREMENTS }}
python_requires = >=3.7
include_package_data = True

[options.packages.find]
where = src

[options.extras_require]
develop =
    pytest

```

4. The package's `pyproject.toml` should use the following template and add any
build-system requirements:

```toml
[build-system]
build-backend = "setuptools.build_meta"
requires = [
  "setuptools>=42",
  "wheel",
]

```

5. `_version.py` should use the following template:

```python
__version__ = "0.0.1"

```

6. `__init__.py` must start with the following:

```python
# removing __version__ import will cause build to fail. see: https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__

```

Further explanation of the rational behind this pattern and more verbose explanation can be found in #12.
