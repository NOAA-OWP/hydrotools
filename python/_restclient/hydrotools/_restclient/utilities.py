#!/usr/bin/env python3

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Hashable, Iterable, Literal, Union

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
