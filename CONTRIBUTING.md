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
git clone git@github.com:{{ user.name }}/evaluation_tools.git && cd evaluation_tools
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
├── my_subpackage/
   ├── evaluation_tools/
   │   └── my_subpackage/
   │       ├── __init__.py
   │       └── foo.py
   │       └── bar.py
   ├── setup.py
   ├── pyproject.toml
   └── tests/
```

3. The package's `setup.py` should use the following template:

```python
#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages

# python namespace subpackage
# this namespace package follows PEP420
# https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

NAMESPACE_PACKAGE_NAME = "evaluation_tools"
SUBPACKAGE_NAME = "{{ SUBPACKAGE_NAME }}"

# Namespace subpackage slug.
# Ex: mypkg.a # Where the namespace pkg = `mypkg` and the subpackage = `a`
SUBPACKAGE_SLUG = f"{NAMESPACE_PACKAGE_NAME}.{SUBPACKAGE_NAME}"

# Subpackage version
VERSION = "0.1.0"

# Package author information
AUTHOR = "{{ AUTHOR }}"
AUTHOR_EMAIL = "{{ AUTHOR_EMAIL }}"

# Short sub-package description
DESCRIPTION = "{{ SHORT_DESCRIPTION }}"

# Package dependency requirements
REQUIREMENTS = []

setup(
    name=SUBPACKAGE_SLUG,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=["Private :: Do Not Upload to pypi server",],
    description=DESCRIPTION,
    namespace_packages=[NAMESPACE_PACKAGE_NAME],
    packages=find_namespace_packages(
        include=[f"{NAMESPACE_PACKAGE_NAME}.*"]
    ),
    install_requires=REQUIREMENTS,
)
```

4. The package's `pyproject.toml` should use the following template and add any
build-system requirements:

```
[build-system]
build-backend = "setuptools.build_meta"
requires = [
  "setuptools>=42",
  "wheel",
]

```

5. The _package_ level (not subpackage) `setup.py` dictionary `SUBPACKAGES`
should be updated to include the subpackage slug (i.e.
`evaluation_tools.my_subpackage`) and the relative path to the subpackage
(i.e. `python/my_subpackage`).

Example:
```python
# setup.py

SUBPACKAGES ={
    ...,
    "evaluation_tools.my_subpackage": "python/my_subpackage",
}
```

Further explanation of the rational behind this pattern and more verbose explanation can be found in #12.
