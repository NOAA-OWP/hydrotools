"""USGS OGC API URL builders."""
from typing import Optional, Sequence, Any

from yarl import URL
from multidict import MultiDict

from .client_config import SETTINGS
from .constants import OGCAPI, OGCPATH, USGSCollection

QueryType = dict[str, Any] | MultiDict[str] | Sequence[tuple[str, Any]]
"""Type alias for USGS OGC API compatible queryables."""

def build_request(
    server: URL = SETTINGS.usgs_base_url,
    api: OGCAPI = SETTINGS.default_api,
    endpoint: USGSCollection = SETTINGS.default_collection,
    path: OGCPATH = SETTINGS.default_path,
    feature_id: Optional[str] = None,
    query: Optional[QueryType] = None
) -> URL:
    """Constructs a single yarl.URL.

    Args:
        feature_id: Optional specific identifier (e.g., 'USGS-01013550').
        query: Query parameters to add or override default_query.

    Returns:
        A yarl.URL object.
    """
    # Start with the base structure
    url = server / api / endpoint / path

    if feature_id:
        url = url / feature_id

    # Merge defaults with provided params
    query_params = MultiDict(SETTINGS.default_query)
    if query:
        query_params.update(query)

    return url.with_query(query_params)

def build_request_batch(
    feature_ids: Sequence[str],
    queries: Sequence[QueryType]
) -> list[URL]:
    """Constructs a list of yarl.URL objects for paired IDs and queries.

    Args:
        feature_ids: Sequence of specific feature identifiers.
        queries: Sequence of query parameters corresponding to each ID.

    Returns:
        A list of yarl.URL objects.

    Raises:
        ValueError: If the lengths of feature_ids and queries do not match.
    """
    if len(feature_ids) != len(queries):
        raise ValueError(
            f"Mismatched input lengths: feature_ids has {len(feature_ids)} items, "
            f"but queries has {len(queries)} items. Sequences must be of equal length."
        )
    return [build_request(feature_id=f, query=q) for f, q in zip(feature_ids, queries)]

def build_request_batch_from_feature_ids(
    feature_ids: Sequence[str]
) -> list[URL]:
    """Constructs a list of yarl.URL objects for a sequence of feature IDs.

    Args:
        feature_ids: Sequence of specific feature identifiers.

    Returns:
        A list of yarl.URL objects.
    """
    return [build_request(feature_id=f) for f in feature_ids]

def build_request_batch_from_queries(
    queries: Sequence[QueryType]
) -> list[URL]:
    """Constructs a list of yarl.URL objects for a sequence of query dictionaries.

    Args:
        queries: Sequence of query parameters to add or override default_query.

    Returns:
        A list of yarl.URL objects.
    """
    return [build_request(query=q) for q in queries]
