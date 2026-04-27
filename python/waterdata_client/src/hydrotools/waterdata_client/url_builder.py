"""USGS OGC API URL builders."""
from typing import Optional, Sequence, Any, Protocol

from yarl import URL
from multidict import MultiDict

from .client_config import SETTINGS
from .constants import OGCAPI, OGCPATH, USGSCollection

QueryType = dict[str, Any] | MultiDict[Any] | Sequence[tuple[str, Any]]
"""Type alias for USGS OGC API compatible queryables."""

class RequestBuilder(Protocol):
    """Defines a Protocol for a callable object that builds USGS OGC compliant
    URLS.
    
    Args:
        feature_id: Optional specific feature identifier.
        query: Optional query parameters.
    
    Returns:
        A yarl.URL object.
    """
    def __call__(
            self,
            feature_id: Optional[str] = None,
            query: Optional[QueryType] = None
        ) -> URL: ...

def build_request(
    feature_id: Optional[str] = None,
    query: Optional[QueryType] = None,
    server: URL = SETTINGS.usgs_base_url,
    api: OGCAPI = SETTINGS.default_api,
    endpoint: USGSCollection = SETTINGS.default_collection,
    path: OGCPATH = SETTINGS.default_path
) -> URL:
    """Constructs a single yarl.URL.

    Args:
        feature_id: Optional specific feature identifier.
        query: Optional query parameters.
        server: The root URL for USGS OGC API services.
            URL('https://api.waterdata.usgs.gov/ogcapi/v0')
        api: USGS OGC API (e.g. 'collections').
        endpoint: USGS OGC API collection (e.g. 'continuous').
        path: USGS OGC path (e.g. 'items')

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

    # Sanitize booleans
    sanitized_query = MultiDict([
        (str(k), (str(v).lower()) if isinstance(v, bool) else v)
        for k, v in query_params.items()])

    return url.with_query(sanitized_query)

def build_request_batch(
    feature_ids: Sequence[str],
    queries: Sequence[QueryType],
    request_builder: RequestBuilder = build_request
) -> list[URL]:
    """Constructs a list of yarl.URL objects for paired IDs and queries.

    Args:
        feature_ids: Sequence of specific feature identifiers.
        queries: Sequence of query parameters corresponding to each ID.
        request_builder: A callable that builds URLs.

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
    return [request_builder(feature_id=f, query=q) for f, q in zip(feature_ids, queries)]

def build_request_batch_from_feature_ids(
    feature_ids: Sequence[str],
    request_builder: RequestBuilder = build_request
) -> list[URL]:
    """Constructs a list of yarl.URL objects for a sequence of feature IDs.

    Args:
        feature_ids: Sequence of specific feature identifiers.
        request_builder: A callable that builds URLs.

    Returns:
        A list of yarl.URL objects.
    """
    return [request_builder(feature_id=f) for f in feature_ids]

def build_request_batch_from_queries(
    queries: Sequence[QueryType],
    request_builder: RequestBuilder = build_request
) -> list[URL]:
    """Constructs a list of yarl.URL objects for a sequence of query dictionaries.

    Args:
        queries: Sequence of query parameters to add or override default_query.
        request_builder: A callable that builds URLs.

    Returns:
        A list of yarl.URL objects.
    """
    return [request_builder(query=q) for q in queries]
