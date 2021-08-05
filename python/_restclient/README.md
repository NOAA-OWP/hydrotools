# OWPHydroTools :: REST Client

Subpackage of objects and utilities suitable for quickly developing robust
REST api libraries.

Main features:

- `RestClient`: a class which offers asynchronous performance via a convenient serial
  wrapper, sqlite database GET request caching, GET request backoff, batch GET requests,
  and flexible url argument encoding.

- `Url`: Treat urls like to `pathlib.Path`s. Supports appending paths with `/` and
  appending url query parameters with `+`.

- `ClientSession`: Extension of
  [`aiohttp_client_cache`](https://github.com/JWCook/aiohttp-client-cache) that adds
  exponential backoff.

- `Variadic`: Join list or tuple of objects on some delimiter. Useful when query
  parameters utilize a non-`key=value&key=value2` pattern.

- `Alias` and `AliasGroup`: Immutable utility classes that simplify common API library
  development patterns (i.e. separation of backend uris from front end interfaces).

See the [REST Client
Documentation](https://noaa-owp.github.io/hydrotools/hydrotools._restclient.html) for a
complete list and description of the currently available methods. To report bugs or
request new features, submit an issue through the [OWPHydroTools Issue
Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

## Installation

In accordance with the python community, we support and advise the usage of virtual
environments in any workflow using python. In the following installation guide, we
use python's built-in `venv` module to create a virtual environment in which the
tool will be installed. Note this is just personal preference, any python virtual
environment manager should work just fine (`conda`, `pipenv`, etc. ).

```bash
# Create and activate python environment, requires python >= 3.8
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip

# Install _restclient
$ python3 -m pip install hydrotools._restclient
```

## Usage

The following example demonstrates how one might use `hydrotools._restclient` to write a simple REST api interface.

### Code

```python
from hydrotools import _restclient


class BaconIpsum:
    """ Python API to baconipsum.com. """

    _base_url = "https://baconipsum.com/api/"

    # Return "meat-and-filler" if "mixed-meat" or "mixed" passed like:
    # _meat_and_filler["mixed-meat"] or _meat_and_filler.get("mixed")
    _meat_and_filler = _restclient.Alias("meat-and-filler", ["mixed-meat", "mixed"])
    _all_meat = _restclient.Alias("all-meat", ["all-meat", "all"])

    # Treat multiple alias as one alias
    _meat_options = _restclient.AliasGroup([_meat_and_filler, _all_meat])

    def __init__(self):
        self._restclient = _restclient.RestClient(
            self._base_url,
            cache_filename="bacon_ipsum_cache",
            cache_expire_after=43200, # in seconds
            n_retries=5,
        )

    @classmethod
    def get(cls, type: str):
        """
        Get either 'mixed-meat' / 'mixed' or 'all-meat' / 'all'
        Mixed contains filler 'lorem ipsum' text. All is just the meats!
        """
        inst = cls()

        params = {"type": inst._meat_options[type], "sentences": 1, "format": "json"}

        response = inst._restclient.get(parameters=params)
        return response.json()


if __name__ == "__main__":
    print(BaconIpsum.get("all-meat"))

    print(BaconIpsum.get("mixed"))
```

### Output

```console
['Short loin tongue drumstick chuck beef meatball brisket ball tip pork loin doner kielbasa flank.']
['Andouille excepteur in, shankle irure laboris voluptate et ad incididunt.']
```
