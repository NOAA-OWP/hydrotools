"""JSON Schema extraction utility functions."""
import keyword
import re
from typing import Any
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
