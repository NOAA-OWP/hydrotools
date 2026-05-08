"""JSON Schema extraction utility functions."""
import keyword
import re
from typing import Any, Optional, TypedDict
import builtins

OPENAPI_TO_PYTHON_TYPES: dict[str, str] = {
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
    field_constraints: str

class CollectionMetadata(TypedDict):
    """Defines collection metadata used by Jinja2 templates."""
    value: str
    enum_member: str
    class_name: str
    request_model: str
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

def get_type_hint(
        type_schema: dict[str, Any], required: bool = False
) -> tuple[str, Any, dict[str, Any]]:
    """Returns type hint, default value, and pydantic field constraints.

    Args:
        type_schema: 'schema' object in OpenAPI JSON schema parameter.
        required: If False, designates type as 'Optional'. Defaults to False.
    
    Returns:
        type_hint, default_value, field_constraints.
    
    Raises:
        ValueError if unable to determine type.
    """
    # Check for empty schema
    if not type_schema:
        raise ValueError("Schema is empty. Unable to determine type.")

    # Get base type
    oa_type = type_schema.get("type", "string")
    type_hint = OPENAPI_TO_PYTHON_TYPES.get(oa_type, "str")
    default = type_schema.get("default")

    # Handle string
    if oa_type == "string":
        # Add quotes to string default
        if default:
            default = f'"{default}"'

        # Handle URI types
        if type_schema.get("format") == "uri":
            type_hint = "URL"

    # Handle array
    if oa_type == "array":
        item_schema = type_schema.get("items", {})
        oa_element_type = item_schema.get("type", "string")
        element_type = OPENAPI_TO_PYTHON_TYPES.get(oa_element_type)

        # Handle URI
        if oa_element_type == "string":
            if type_schema.get("format") == "uri":
                element_type = "URL"

        # Handle enum
        if item_schema.get("enum"):
            enums = ", ".join(f'"{v}"' for v in item_schema.get("enum", []))
            element_type = f"Literal[{enums}]"

        type_hint = f"{type_hint}[{element_type}]"

    # Handle enum
    if type_schema.get("enum"):
        enums = ", ".join(f'"{v}"' for v in type_schema.get("enum", []))
        type_hint = f"Literal[{enums}]"

    # Handle optional
    if not required:
        type_hint = f"Optional[{type_hint}]"

    # Build Field arguments
    field_args = {
        "frozen": True,
        "default": default
    }

    # Update field arguments
    field_map = [
        ("ge", type_schema.get("minimum")),
        ("le", type_schema.get("maximum")),
        ("pattern", type_schema.get("pattern")),
        ("min_length", type_schema.get("minLength")),
        ("max_length", type_schema.get("maxLength"))
    ]
    field_args.update({k: v for k, v in field_map if v is not None})

    return type_hint, default, field_args

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
    parsed: list[ParameterMetadata] = []
    for param in param_list:
        # Limit to query parameters (ignore path/header parameters)
        if param.get("in") != "query":
            continue

        # Extract
        name = param.get("name")

        # Validate name
        if name is None:
            raise KeyError(f"Unable to parse parameter {param}, no value for 'name'")

        # Attempt to make valid argument from parameter
        python_name = validate_identifier(
            to_snake_case(name),
            fix_errors=True,
            error_prefix="query_"
            )

        # Validate
        try:
            python_name = validate_identifier(python_name)
        except SyntaxError as e:
            raise SyntaxError(f"Unable to make `{name}` a valid Python identifier.") from e

        # Extract type information
        required = param.get("required", False)
        type_hint, default_value, field_constraints = get_type_hint(
            param.get("schema", {}), required)

        # Set parameter description
        parameter_description: str = param.get("description", "")
        short_description = parameter_description.replace(
            "\n", " ").replace('"', " ").split(".", 1)[0].strip()

        # Convert field constraints to strings
        field_constraints.update({"description": f'"{short_description}."'})
        arguments = [f"{k}={v}" for k, v in field_constraints.items()]

        parsed.append({
            "name": name,
            "python_name": python_name,
            "type_hint": type_hint,
            "description": parameter_description,
            "default": default_value,
            "field_constraints": ", ".join(arguments)
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
    collections: list[CollectionMetadata] = []
    paths = schema.get("paths", {})

    for path, details in paths.items():
        # Match pattern: /collections/{collectionId}/items
        match = re.search(r"/collections/(?P<cid>[^/]+)/items/?$", path)
        if match:
            cid = match.group("cid")
            enum_member = to_screaming_snake_case(cid)
            class_name = f"{to_pascal_case(cid)}Client"
            request_model = f"{to_pascal_case(cid)}Request"

            # Validate enum member and class name
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
                request_model = validate_identifier(
                    request_model,
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
                "request_model": request_model,
                "description": endpoint_information.get("description", f"Client for {cid}."),
                "parameters": sorted(parameters, key=lambda x: x["python_name"])
            })

    # Return sorted by value for a deterministic file
    return sorted(collections, key=lambda x: x["class_name"])
