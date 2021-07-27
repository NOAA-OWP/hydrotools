import urllib.parse as parse
from typing import Dict, List, Tuple, Union, TypeVar
from collections import UserString
import re

# local imports
from ._iterable_nonstring import IterableNonStringLike
from .urllib_types import Quote, QUOTE_PLUS_OR_CARRY, FORWARD_SLASH

__all__ = ["Url", "Variadic"]

PRIMITIVE = TypeVar("PRIMITIVE", bool, float, int, str, None)


class Url(UserString, str):
    """
    Treat urls analogous to pathlib.Path's treatment of paths.

    Examples:
        Concatenate urls using the forward slash operator (see equivalent `Url.joinurl`)
        >>> url = Url("https://www.test.gov") / "api" / "feature"
        >>> print(url)
        >>> https://www.test.gov/api/feature

        Append url query using the plus operator (see equivalent `Url.add` method)
        >>> url = url + {"format": "json", "sites": [1,2,3]}
        >>> print(url)
        >>> https://www.test.gov/api/feature?format=json&sites=1&sites=2&sites=3

        Automagically unquote urls
        >>> o = Url("https://www.test.gov/?quoted=%27args%27")
        >>> print(o)
        >>> https://www.test.gov/?quoted='args'
        >>> # Re-quote the url
        >>> print(o.quote_url)
        >>> https://www.test.gov/?quoted=%27args%27

        Supports comparing quoted and unquoted urls
        >>> o = Url("https://www.test.gov/?quoted=%27args%27")
        >>> o2 = Url("https://www.test.gov/?quoted='args'")
        >>> assert o == o2 # True

        Note:
        By default, the "/" is treated as a safe character that is not escaped in url
        path's and query's. This can be changed with the `safe` key word argument.
        Likewise, url path's and query's are quoted using urllib.parse.quote_plus, where
        spaces are replaced with `+`s to support building queries. Urls are unquoted
        using urllib.parse.unquote_plus to mirror the behavior when unquoting.  To
        change this behavior, use the `quote_treatment` keyword argument and pass a
        member from the `hydrotools._restclient.Quote` enum. Options are `Quote.QUOTE`,
        `Quote.QUOTE_PLUS`, or `Quote.QUOTE_FROM_BYTES`. The `quote_overide_map` option
        allows explicit remapping of a character or set of characters in the encoded
        form of the url. An example use of `quote_overide_map` is to remap `+` to `%2B`,
        its escaped literal form. This behavior is not supported in `urllib.parse` which
        either does not escape `+` or escapes it as `%20`.  `Url` instances passed to
        `Url` (e.g.  `Url(Url("http://www.test.gov", quote_treatment=Quote.QUOTE,
        safe="/+"))` retain non-default quote and safe options unless a non-default
        `quote_treatment` / `safe` / `quote_overide_map` value is specified
        respectively.

        urls are unquoted at construction time for `Url` object comparison sake
        equivalency and readability.

        url query parameter values passed as either a list or tuple are represented with
        individual `key=value` pairs each seperated by the `&` (i.e. {"key": ["v_0",
        "v_1"]} -> key=v_0&key=v_1).

    """

    def __new__(
        cls,
        url: Union[str, "Url"],
        *,
        quote_treatment: Quote = QUOTE_PLUS_OR_CARRY,
        safe: str = FORWARD_SLASH,
        quote_overide_map: Dict[str, str] = {},
    ):
        # Overload so unquote_treatment kwarg does not raise TypeError for str()
        return str.__new__(cls, url)

    def __init__(
        self,
        url: Union[str, "Url"],
        *,
        quote_treatment: Quote = QUOTE_PLUS_OR_CARRY,
        safe: str = FORWARD_SLASH,
        quote_overide_map: Dict[str, str] = {},
    ) -> None:
        is_url_instance = isinstance(url, Url)

        # py3.8+ checking with `is` throws warning if is literal. Using == instead
        if quote_treatment == QUOTE_PLUS_OR_CARRY:
            # set default: carry quote treatment if url is Url instance, else quote_plus
            quote_treatment = (
                Quote.QUOTE_PLUS if not is_url_instance else url._quote_treatment
            )

        if safe == FORWARD_SLASH:
            # set default: carry safe characters if url is Url instance, else "/"
            safe = "/" if not is_url_instance else url._safe

        # fail fast if invalid unquote_treatment
        if not quote_treatment in Quote:
            error_message = "quote_treatment must be member of Quote Enum."
            raise ValueError(error_message)

        if is_url_instance:
            if not quote_overide_map:
                # set default: carry safe characters if url is Url instance, else "/"
                quote_overide_map = url._quote_overide_map
            url = url.url

        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"

        self._url = parse.urlparse(url)

        self._safe = safe
        self._quote_treatment = quote_treatment
        self._quote_overide_map = quote_overide_map.copy()
        self._validate_construction(self._url)
        self._url = self._clean_parse_result(
            self._url, unquote_treatment=self._quote_treatment
        )
        self.data = self._url.geturl()

    def __add__(self, b: Dict[str, Union[str, List[str]]]) -> "Url":
        """Add/append query parameters to `Url` object using `+` operator. See `Url.add`
        for further details. Methods are equivalent.

        Example
        -------
        >>> url = Url("https://www.test.gov") / "api" / "feature"
        >>> url = url + {"format": "json", "sites": [1,2,3]}
        >>> print(url)
        >>> https://www.test.gov/api/feature?format=json&sites=1&sites=2&sites=3
        """
        return self.add(b)

    def add(self, b: Dict[str, Union[PRIMITIVE, List[PRIMITIVE]]]) -> "Url":
        """Add/append query parameters to `Url` object url via a dictionary. Dictionary
        values are either specified as either a primitive or list of primitives. Url
        query parameter values passed in list are represented with individual
        `key=value` pairs each seperated by the `&` (i.e. {"key": ["v_0", "v_1"]} ->
        key=v_0&key=v_1).


        Parameters
        ----------
        b : Dict[str, Union[PRIMITIVE, List[PRIMITIVE]]]
            mapping of query keywords to query values

        Returns
        -------
        Url
            New Url instance including provided query parameters

        Example
        -------
        >>> url = Url("https://www.test.gov") / "api" / "feature"
        >>> url = url.add({"format": "json", "sites": [1,2,3]})
        >>> # or equivalently
        >>> url = url + {"format": "json", "sites": [1,2,3]}
        >>> print(url)
        >>> https://www.test.gov/api/feature?format=json&sites=1&sites=2&sites=3
        """
        query = parse.parse_qs(self._url.query)  # type: dict[list[str]]
        # compare keys
        intersect = set(query) & set(b)
        left_difference = {k: b[k] for k in set(b) - set(query)}

        # put keys from b not in self in self
        query.update(left_difference)

        # append values from b to keys existing in self
        for k in intersect:
            to_insert = b[k] if isinstance(b[k], IterableNonStringLike) else [b[k]]
            query[k].extend(to_insert)

        # Transform query from dict to string of kwargs
        query = parse.urlencode(
            query,
            doseq=True,
            quote_via=self._quote_treatment.quote_style,
            safe=self._safe,
        )
        return self._build_parse_result_cast_to_url(
            self._url,
            query=query,
            quote_treatment=self._quote_treatment,
            safe=self._safe,
            quote_overide_map=self._quote_overide_map,
        )

    def __truediv__(self, b: str) -> "Url":
        """Append path to `Url` object url.  See `Url.joinurl` for further details.
        Methods are equivalent.

        Parameters
        ----------
        b : str
            Path appended to url of new `Url` instance

        Returns
        -------
        Url
            New Url instance with appended path, `b`.

        Example
        -------
        >>> url = Url("https://www.test.gov")
        >>> url = url / "api"
        >>> print(url)
        >>> https://www.test.gov/api
        """
        return self.joinurl(b)

    def joinurl(self, b: str) -> "Url":
        """Append path to `Url` url. Erronenous `/`s are automatically removed. A single
        trailing `/` is respected if desired but will not be included if not specified.

        Urls can also be joined using the `/` opporator. This is equivalent to calling
        the `Url.joinurl` method. As such, it is recommended to use the more idiomatic
        `/` opporator.


        Parameters
        ----------
        b : str
            url path to append

        Returns
        -------
        Url
            New Url instance with appended path, `b`.

        Example
        -------
        >>> url = Url("https://www.test.gov")
        >>> url.joinurl("api")
        >>> # or equivalently
        >>> url = url / "api"
        >>> print(url)
        >>> https://www.test.gov/api
        """
        if isinstance(b, str):
            path = f"{self._url.path}/{b}"
            return self._build_parse_result_cast_to_url(
                self._url,
                path=path,
                quote_treatment=self._quote_treatment,
                safe=self._safe,
                quote_overide_map=self._quote_overide_map,
            )
        raise TypeError("Arg is required subclass string")

    @property
    def quote_treatment(self) -> str:
        """ Method for handling quoted characters """
        return self._quote_treatment

    @property
    def url(self) -> str:
        """ Unquoted string representation of url """
        return str(self)

    @property
    def quote_url(self) -> str:
        """Quoted string representation of url. Urls quoted using
        urllib.parse.quote_plus."""
        # serialized query from str/encoded to dict
        query = parse.parse_qs(self._url.query)  # type: dict[str, list[str]]

        # quote url path
        path = self._quote_treatment.quote(self._url.path, safe=self._safe)
        # Note: list items treated as -> item=1&item=2 not item=%5B1%2C+2%5D
        query = parse.urlencode(
            query,
            doseq=True,
            quote_via=self._quote_treatment.quote_style,
            safe=self._safe,
        )
        url = self._build_parse_result(self._url, path=path, query=query).geturl()
        # Explicitly replace characters in url
        for char, remap_char in self._quote_overide_map.items():
            url = url.replace(char, remap_char)
        return url

    @staticmethod
    def _validate_construction(url: parse.ParseResult):
        # ensure `netloc` property is set
        required_properties = ["netloc"]
        required_set = _are_properties_set(url, required_properties)

        # Fail fast
        if not required_set:
            raise ValueError(f"invalid url, requires {required_properties}.")

    @staticmethod
    def _clean_parse_result(
        url: parse.ParseResult,
        unquote_treatment: Quote = Quote.QUOTE_PLUS,
    ) -> parse.ParseResult:
        assert unquote_treatment in Quote

        # remove repeated occurrence of /
        path = re.sub("//+", "/", url.path)
        # unquote query args for readability
        query = unquote_treatment.unquote(url.query)

        return Url._build_parse_result(url, path=path, query=query)

    @staticmethod
    def _build_parse_result(
        url: parse.ParseResult,
        *,
        scheme=None,
        netloc=None,
        path=None,
        params=None,
        query=None,
        fragment=None,
    ) -> parse.ParseResult:
        return parse.ParseResult(
            scheme=scheme if scheme is not None else url.scheme,
            netloc=netloc if netloc is not None else url.netloc,
            path=path if path is not None else url.path,
            params=params if params is not None else url.params,
            query=query if query is not None else url.query,
            fragment=fragment if fragment is not None else url.fragment,
        )

    @staticmethod
    def _build_parse_result_cast_to_url(
        url: parse.ParseResult,
        *,
        quote_treatment: Quote = QUOTE_PLUS_OR_CARRY,
        safe: str = FORWARD_SLASH,
        quote_overide_map: Dict[str, str] = {},
        **kwargs,
    ) -> "Url":
        result = Url._build_parse_result(url, **kwargs)
        return Url(
            result.geturl(),
            quote_treatment=quote_treatment,
            safe=safe,
            quote_overide_map=quote_overide_map,
        )


def _are_properties_set(obj: object, properties: Union[List[str], Tuple[str]]) -> bool:
    return all([getattr(obj, prop, None) for prop in properties])


class Variadic(UserString, str):
    """join list or tuple on some delimeter. The is useful when specifying arguments in
    a URL that do not conform to the &key=value&key=value2 convention.

    Example:
        >>> from hydrotools.restclient import ClientSession, Url, Variadic
        >>> url = Url("https://www.test.gov")
        >>> url = url + {"this": Variadic(["that", "the", "other"])}
        >>> print(url.url)
        >>> https://www.test.gov/?this=that,the,other
    """

    def __init__(self, values: Union[List, Tuple], *, delimeter: str = ",") -> None:
        self.data = delimeter.join([str(v) for v in values])

    def encode(self, encoding: str = ..., errors: str = ...) -> bytes:
        kwargs = {}
        if encoding is not Ellipsis:
            kwargs["encoding"] = encoding
        if errors is not Ellipsis:
            kwargs["errors"] = errors

        return self.data.encode(**kwargs)
