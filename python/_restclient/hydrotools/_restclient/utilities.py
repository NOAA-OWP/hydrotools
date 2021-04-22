#!/usr/bin/env python3

from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Hashable, Iterable, List, Union

# local import
from ._iterable_nonstring import IterableNonStringLike


@dataclass(frozen=True)
class Alias:
    """Create an immutable one to many relationship where a set of keys alias some value. This is often
    useful in a variety of applications when the API differs from the backend value.
    This is also useful when writing factories patterns.

    A value can be any scalar, callable, tuple, or frozenset type. At construction,
    value is deepcopied, meaning a value cannot be mutated by reference. Valid alias
    keys are scalar types and collections of scalar types. Keys are stored in a
    frozenset, so in the case of passing a dictionary as the keys arg, only the
    dictionary keys from the passed dictionary will be considered as keys.

    Examples:
        cms = Alias("cms", ["CMS", "m^3/s"])

        cms["CMS"] # returns "cms"
        cms.get("m^3/s") # returns "cms"
        "CMS" in cms # returns True

        # foo is callable
        foo_alias = Alias(foo, ["bar", "baz"])

        result = foo_alias["bar"]()
    """

    value: Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]
    keys: Union[Iterable, Hashable]

    def __post_init__(self):

        scalar_or_callable = Union[
            int, float, str, bytes, bool, Callable, tuple, frozenset, None
        ]

        if not isinstance(self.value, scalar_or_callable.__args__):
            error_message = f"value must be type {str(scalar_or_callable.__args__)}"
            raise ValueError(error_message)

        # Create deep copy so a ref to a mutable value could not change keys implicitly
        self.__dict__["value"] = deepcopy(self.value)

        # If non- str/bytes collection, frozenset, else frozenset([keys])
        self.__dict__["keys"] = (
            frozenset(self.keys)
            if isinstance(self.keys, IterableNonStringLike)
            else frozenset([self.keys])
        )

        if isinstance(self.value, Alias):
            # Alias is passed as value, use contents to extend into new instance
            self.__dict__["keys"] = self.keys | self.value.keys
            self.__dict__["value"] = self.value.value

    def get(
        self, value: Hashable
    ) -> Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]:
        """Get value given a valid alias value. If a valid value is not provided, return
        None.

        Parameters
        ----------
        value : Hashable
            Valid alias value

        Returns
        -------
        Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]
           alias value if valid value, else None
        """
        if value in self:
            return self.value

        return None

    def __contains__(self, value) -> bool:
        return value in self.keys

    def __getitem__(
        self, value
    ) -> Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]:
        value = self.get(value)

        if value is None:
            raise ValueError(
                f"Invalid value {str(value)}. Valid values are {str(self.keys)}"
            )

        return value

    def __or__(self, b):
        if not isinstance(b, Alias):
            error_message = f"{b} must be type Alias"
            raise TypeError(error_message)

        return AliasGroup([self, b])

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{str(self.value)}: {str(self.keys)}"


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
            symmetric_differences = member.keys ^ symmetric_differences
            union = member.keys | union

            for key in member.keys:
                self.option_map[key] = member

        duplicate_value = union - symmetric_differences

        if duplicate_value:
            raise ValueError(f"Repeated valid_value {duplicate_value} not allowed")

    def get(
        self, value: Hashable
    ) -> Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]:
        """Get singular Alias value from group when provided valid alias value. If a
        valid value is not provided, return None.

        Parameters
        ----------
        value : Hashable
            Valid alias value

        Returns
        -------
        Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]
           alias value if valid value, else None
        """
        option = self.option_map.get(value)

        if option is None:
            return None

        return option.value

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
