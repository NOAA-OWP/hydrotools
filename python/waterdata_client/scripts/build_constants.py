"""Run this script to generate and write the `constants.py` file using the Jinja2
template and the "items" collections found in the USGS OGC API schema.

# Usage
The following assumes you are developing in an UNIX-like environment and using a
Python virtual environment called "env".

```bash
$ git clone git@github.com:NOAA-OWP/hydrotools.git
$ cd hydrotools/python/waterdata_client
$ python3 -m venv env
$ source env/bin/activate
(env) $ python3 -m pip install -U pip wheel
(env) $ pip install -e .[develop]
(env) $ python3 scripts/build_constants.py ./templates/ --output src/hydrotools/waterdata_client/constants.py
```
"""
import keyword
from pathlib import Path
import re
from typing import Any
from datetime import datetime, UTC
import click
from jinja2 import Environment, FileSystemLoader
from hydrotools.waterdata_client.schema import get_schema
from hydrotools.waterdata_client.client_config import SETTINGS
from hydrotools.waterdata_client._version import __version__

def get_template_data(
        schema: dict[str, Any],
        ignore_errors: bool = False,
        fix_errors: bool = False,
        error_prefix: str = "COLLECTION_"
    ) -> list[dict[str, str]]:
    """Extracts collection metadata for the constants template.
    
    Args:
        schema: Deserialized dict derived from USGS OGC API schema.
        ignore_errors: If True, skips collections with invalid Python identifier
            characters. If False, raises. Defaults to False.
        fix_errors: If True, prepend error_prefix to erroneous collection labels.
            Defaults to False.
        error_prefix: String added to front of collection enumeration value, if
            fix_errors is True. Defaults to 'COLLECTION_'.
    
    Returns:
        List of extracted mappings (dict) from enum members in screaming
            SNAKE_CASE to enum values for use with Jinja2 StrEnum building
            template.
    
    Raises:
        SyntaxError if unable to translate collection label to valid Python
            identifier.
    """
    collections = []
    paths = schema.get("paths", {})

    for path in paths.keys():
        # Match pattern: /collections/{collectionId}/items
        match = re.search(r"/collections/(?P<cid>[^/]+)/items/?$", path)
        if match:
            cid = match.group("cid")
            enum_member = cid.upper().replace("-", "_").replace(".", "_")

            # Validate identifier
            if not enum_member.isidentifier() or keyword.iskeyword(enum_member):
                if ignore_errors:
                    continue
                elif fix_errors:
                    enum_member = f"{error_prefix}{enum_member}"
                else:
                    raise SyntaxError(f"{enum_member} is not a valid identifier")
            collections.append({
                "enum_member": enum_member,
                "value": cid
            })

    # Return sorted by value for a deterministic file
    return sorted(collections, key=lambda x: x["value"])

@click.command()
@click.argument("templates", type=click.Path(exists=True, file_okay=False,
    dir_okay=True, path_type=Path))
@click.option("-n", "--name", nargs=1, type=str, default="constants.py.j2",
    help="Output file name.")
@click.option("-o", "--output", nargs=1, type=click.Path(
    exists=False, file_okay=True, dir_okay=False, path_type=Path, allow_dash=True),
    help="Output file path", default="-") # NOTE: "-" means stdout
@click.option('--overwrite/--no-overwrite', default=False,
    help="Overwrite existing file, disabled by default")
@click.option('--ignore-errors/--no-ignore-errors', default=False,
    help="Ignore non-Python friendly collection labels, disabled by default")
@click.option('--fix-errors/--no-fix-errors', default=False,
    help="Attempt to fix incompatible collection labels, disabled by default.")
@click.option("-p", "--prefix", nargs=1, type=str, default="COLLECTIONS_",
    help="If fix-errors enabled, prepends this to problematic labels. Defaults to 'COLLECTIONS_'")
def write_constants_module(
        templates: Path,
        name: str,
        output: Path,
        overwrite: bool = False,
        ignore_errors: bool = False,
        fix_errors: bool = False,
        prefix: str = "COLLECTION_"
) -> None:
    """Renders the constants.py file from the OGC schema.

    \b
    Args:
        templates: File system directory containing Jinja2 template files.
        name: Template file name. Defaults to 'constants.py.j2'.
        output: The location to write the resulting file. Defaults to stdout.
        overwrite: If true, overwrite the file if it exists. Defaults to false.
        ignore_errors: If True, skips collections with invalid Python identifier
            characters. If False, raises.
        fix_errors: If True, prepend error_prefix to erroneous collection labels.
            Defaults to False.
        prefix: String added to front of collection enumeration value, if
            fix_errors is True. Defaults to 'COLLECTION_'.
    
    \b
    Raises:
        FileExistsError: If the file exists and overwrite is False.
    """
    # Check for file
    if output.exists() and not overwrite:
        raise FileExistsError(f"{output} already exists")

    # Resolve schema
    schema = get_schema()
    template_data = get_template_data(
        schema, ignore_errors=ignore_errors, fix_errors=fix_errors,
        error_prefix=prefix)

    # Metadata
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S Z")

    # Setup Jinja2
    env = Environment(
        loader=FileSystemLoader(templates),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Render and save
    template = env.get_template(name=name)
    content = template.render(
        timestamp=timestamp,
        schema_source=str(SETTINGS.schema_url),
        schema_version=schema.get("info", {}).get("version", "UNKNOWN"),
        openapi_version=schema.get("openapi", "UNKNOWN"),
        collections=template_data,
        package_version=__version__,
        script_name=Path(__file__).name
        )
    with click.open_file(output, "w", encoding="utf-8") as fo:
        fo.write(content)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    write_constants_module()
