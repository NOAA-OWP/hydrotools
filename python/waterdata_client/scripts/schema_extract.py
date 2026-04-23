"""JSON Schema extraction utility functions."""
import keyword
import re
from typing import Any, Optional, TypedDict
import builtins
from hydrotools.waterdata_client._version import __version__

JSON_TO_PYTHON_TYPES = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "array": "Sequence",
    "object": "dict"
}
"""Mapping from types in OpenAPI JSON schema types to Python types."""

class ParameterMetadata(TypedDict):
    """Defines API parameter metadata used by Jinja2 templates."""
    name: str
    python_name: str
    type_hint: str
    description: str
    default: str
    required: bool

class CollectionMetadata(TypedDict):
    """Defines collection metadata used by Jinja2 templates."""
    value: str
    enum_member: str
    class_name: str
    description: str
    parameters: list[ParameterMetadata]

def to_screaming_snake_case(
        text: str,
        replace: Optional[dict[str, str]] = None
    ) -> str:
    """Converts kebab-case to SCREAMING_SNAKE_CASE
    (e.g. 'latest-continuous' -> 'LATEST_CONTINUOUS').
    
    Args:
        text: Input kebab-case string.
        replace: Optional mapping from old string elements to new. Defaults to
            {'-': '_', '.': '_'}.
    
    Returns:
        Transformed input string in SCREAMING_SNAKE_CASE.
    """
    # Set replacement elements and make translation table
    if replace is None:
        replace = {'-': '_', '.': '_'}
    table = str.maketrans(replace)

    # Transform
    return text.translate(table).upper()

def to_snake_case(
        text: str,
        replace: Optional[dict[str, str]] = None
    ) -> str:
    """Converts kebab-case to snake_case
    (e.g. 'latest-continuous' -> 'latest_continuous').
    
    Args:
        text: Input kebab-case string.
        replace: Optional mapping from old string elements to new. Defaults to
            {'-': '_', '.': '_'}.
    
    Returns:
        Transformed input string in snake_case.
    """
    # Set replacement elements and make translation table
    if replace is None:
        replace = {'-': '_', '.': '_'}
    table = str.maketrans(replace)

    # Transform
    return text.translate(table).lower()

def to_pascal_case(
        text: str,
        pattern: str = r"[-.]"
    ) -> str:
    """Converts kebab-case to PascalCase.
    (e.g. 'latest-continuous' -> 'LatestContinuous').
    
    Args:
        text: Input kebab-case string.
        pattern: Raw string indicating characters to ignore (drop) from
            resulting PascalCase string. Defaults to r'[-.]'. Passed directly to
            `re.split`.
    
    Returns:
        Transformed input string in PascalCase.
    """
    # Split on ignore characters
    words = re.split(pattern, text)

    # Capitalize and join split words
    return "".join(word.capitalize() for word in words if word)

def validate_identifier(
        identifier: str,
        fix_errors: bool = False,
        error_prefix: str = "ID_"
    ) -> str:
    """Validates and returns valid Python identifier string.
    
    Args:
        identifier: Identifier to be validated.
        fix_errors: If True, prepend error_prefix to erroneous identifier.
            Defaults to False.
        error_prefix: String added to front of identifier, if
            fix_errors is True. Defaults to 'ID_'.
    
    Returns:
        Valid identifier.
    
    Raises:
        SyntaxError if unable to translate identifier to valid Python identifier.
    """
    # Rejection criteria
    reject = [
        not identifier.isidentifier(),
        keyword.iskeyword(identifier),
        identifier in dir(builtins)
    ]
    if any(reject):
        if fix_errors:
            return f"{error_prefix}{identifier}"
        raise SyntaxError(f"{identifier} is not a valid identifier")
    return identifier

def parse_parameters(
        param_list: list[dict[str, Any]]
    ) -> list[ParameterMetadata]:
    """Parse endpoint parameters."""
    parsed = []
    for param in param_list:
        # Limit to query parameters (ignore path/header parameters)
        if param.get("in") != "query":
            continue

        # Extract
        name = param.get("name")

        # Validate name
        if name is None:
            raise ValueError(f"Unable to parse parameter {param}")
        python_name = validate_identifier(
            to_snake_case(name),
            fix_errors=True,
            error_prefix="query_"
            )

        # Extract type information
        schema = param.get("schema", {})
        open_api_type = schema.get("type", "Any")
        enum_values = schema.get("enum", [])

        # Determine Python type hint
        type_hint = JSON_TO_PYTHON_TYPES.get(open_api_type, "str")
        if enum_values:
            formatted_enums = ", ".join(f'"{v}"' for v in enum_values)
            type_hint = f"Literal[{formatted_enums}]"
        match open_api_type:
            case "integer":
                type_hint = "int"
            case "array":
                item_oa_type = schema.get("items", {}).get("type", "str")
                item_py_type = JSON_TO_PYTHON_TYPES.get(item_oa_type, "str")
                sequence_type = JSON_TO_PYTHON_TYPES.get("array", "list")
                type_hint = f"{sequence_type}[{item_py_type}]"

        parsed.append({
            "name": name,
            "python_name": python_name,
            "type_hint": type_hint,
            "description": param.get("description"),
            "default": schema.get("default"),
            "required": param.get("required", False)
        })

    return parsed

def get_template_data(
        schema: dict[str, Any],
        ignore_errors: bool = False,
        fix_errors: bool = False,
        error_prefix: str = "COLLECTION_"
    ) -> list[CollectionMetadata]:
    """Extracts collection metadata for the jinja2 templates.
    
    Args:
        schema: Deserialized dict derived from USGS OGC API schema.
        ignore_errors: If True, skips collections with invalid Python identifier
            characters. If False, raises. Defaults to False.
        fix_errors: If True, prepend error_prefix to erroneous collection labels.
            Defaults to False.
        error_prefix: String added to front of collection enumeration value, if
            fix_errors is True. Defaults to 'COLLECTION_'.
    
    Returns:
        List of extracted metadata for each USGS collection identified.
    
    Raises:
        SyntaxError if unable to translate collection label to valid Python
            identifier.
    """
    collections = []
    paths = schema.get("paths", {})

    for path, details in paths.items():
        # Match pattern: /collections/{collectionId}/items
        match = re.search(r"/collections/(?P<cid>[^/]+)/items/?$", path)
        if match:
            cid = match.group("cid")
            enum_member = to_screaming_snake_case(cid)
            class_name = f"{to_pascal_case(cid)}Client"

            # Validate identifier
            try:
                enum_member = validate_identifier(
                    enum_member,
                    fix_errors=fix_errors,
                    error_prefix=error_prefix
                )
                class_name = validate_identifier(
                    class_name,
                    fix_errors=fix_errors,
                    error_prefix=error_prefix
                )
            except SyntaxError as e:
                if ignore_errors:
                    continue
                raise e

            # Extract endpoint 'get' details
            endpoint_information = details.get("get", {})

            # Extract parameters
            parameters = parse_parameters(
                endpoint_information.get("parameters", [{}])
            )

            # Add collection
            collections.append({
                "value": cid,
                "enum_member": enum_member,
                "class_name": class_name,
                "description": endpoint_information.get("description", f"Client for {cid}."),
                "parameters": sorted(parameters, key=lambda x: x["python_name"])
            })

    # Return sorted by value for a deterministic file
    print(collections)
    return sorted(collections, key=lambda x: x["class_name"])
