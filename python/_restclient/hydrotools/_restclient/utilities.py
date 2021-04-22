#!/usr/bin/env python3

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Hashable, Iterable, List, Union

# local import
from ._iterable_nonstring import IterableNonStringLike


@dataclass(frozen=True)
class Alias:
    """Create an immutable key, value pair where values alias the key. This is often
    useful in a variety of applications when the API differs from the backend value.
    This is also useful when writing factories patterns.

    Any type is a valid key and is deepcopied at construction, meaning keys cannot be
    mutated by reference. Valid alias values are single atomic types and collections
    of atomic types. Values are stored in a frozenset, so in the case of passing a
    dictionary as a value, on the keys from the passed dictionary will be considered.

    Examples:
        cms = Alias("cms", ["CMS", "m^3/s"])

        cms["CMS"] # returns "cms"
        cms.get("m^3/s") # returns "cms"
        "CMS" in cms # returns True

        # foo is callable
        foo_alias = Alias(foo, ["bar", "baz"])

        result = foo_alias["bar"]()
    """

    key: Any
    valid_value: Union[Iterable, Hashable]

    def __post_init__(self):
        # Create deep copy so a ref to a mutable key could not change value implicitly
        self.__dict__["key"] = deepcopy(self.key)

        # If non- str/bytes collection, frozenset, else frozenset([valid_value])
        self.__dict__["valid_value"] = (
            frozenset(self.valid_value)
            if isinstance(self.valid_value, IterableNonStringLike)
            else frozenset([self.valid_value])
        )

        if isinstance(self.key, Alias):
            # Alias is passed as key, use contents to extend into new instance
            self.__dict__["valid_value"] = self.valid_value | self.key.valid_value
            self.__dict__["key"] = self.key.key

    def get(self, value: Hashable) -> Union[Any, None]:
        """Get key given a valid alias value. If a valid key is not provided, return
        None.

        Parameters
        ----------
        value : Hashable
            Valid alias value

        Returns
        -------
        Union[Any, None]
           alias key if valid value, else None
        """
        if value in self:
            return self.key

        return None

    def __contains__(self, value) -> bool:
        return value in self.valid_value

    def __getitem__(self, value) -> Any:
        key = self.get(value)

        if key is None:
            raise ValueError(
                "Invalid value %s. Valid values are %s" % (value, self.valid_value)
            )

        return key

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f"{str(self.key)}: {str(self.valid_value)}"


class AliasGroup:
    """Create a group of Alias objects that are treated like a single Alias. This
    comes in handy to cut down on conditional statements when developing for example,
    rest api libraries. This is clearest shown through an example.

    Example:
        base_url = "www.api.org"

        # In the below, both path-1 and path-2 are different entities.
        # api.org/path-1/cool-feature
        # api.org/path-2/cool-feature

        path_1 = Alias("path-1", [1, "1"])
        path_2 = Alias("path-2", [2, "2"])
        path_group = GroupAlias([path_1, path_2])

        def get_cool_feature(path: Union[int, str]):
            path = path_group[path] # ValueError thrown if invalid path

            url = f"{base_url}/{path}/cool-feature"

            response = requests.get(url)
            return response.json()
    """

    def __init__(self, alias: List[Alias]) -> None:

        for item in alias:
            if not isinstance(item, Alias):
                error_message = "All items must be type `Alias`"
                raise ValueError(error_message)

        self._option_groups = (
            frozenset(alias)
            if isinstance(alias, IterableNonStringLike)
            else frozenset([alias])
        )

        symmetric_differences, union = frozenset(), frozenset()
        self.option_map = {}

        for member in self._option_groups:
            symmetric_differences = member.valid_value ^ symmetric_differences
            union = member.valid_value | union

            for valid_value in member.valid_value:
                self.option_map[valid_value] = member

        duplicate_value = union - symmetric_differences

        if duplicate_value:
            raise ValueError(f"Repeated valid_value {duplicate_value} not allowed")

    def get(self, value: Hashable) -> Union[Any, None]:
        """Get singular Alias key from group when provided valid alias value. If a
        valid key is not provided, return None.

        Parameters
        ----------
        value : Hashable
            Valid alias value

        Returns
        -------
        Union[Any, None]
           alias key if valid value, else None
        """
        option = self.option_map.get(value)

        if option is None:
            return None

        return option.key

    @property
    def option_groups(self):
        return self._option_groups

    def __getitem__(self, value):
        option = self.get(value)

        if option is None:
            raise ValueError(
                "Invalid value %s. Valid values are %s"
                % (value, self.option_map.keys())
            )

        return option

    def __str__(self) -> str:
        return str(self.option_groups)

    def __repr__(self) -> str:
        return str(self.option_groups)
