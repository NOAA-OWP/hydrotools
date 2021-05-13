from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Hashable, Iterable, List, Union

# local import
from ._iterable_nonstring import IterableNonStringLike


@dataclass(frozen=True)
class Alias:
    """Create an immutable many to one relationship where a set of keys alias some
    value. This is often useful in a variety of applications when the API differs
    from the backend value. This is also useful when writing factories patterns.

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
            int, float, str, bytes, bool, Callable, tuple, frozenset, Alias, None
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
        self, key: Hashable
    ) -> Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]:
        """Get value given a valid key. Providing the value or an `Alias` instance is
        also supported. If a valid value is not provided, return None.

        Parameters
        ----------
        value : Hashable
            Valid alias value

        Returns
        -------
        Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]
           alias value if valid key, value, or `Alias` instance, else None
        """
        if key in self:
            return self.value

        return None

    def __contains__(self, key) -> bool:
        def instance_and_value(k):
            if isinstance(k, Alias):
                return k.value == self.value
            return False

        return key in self.keys or key == self.value or instance_and_value(key)

    def __getitem__(
        self, key
    ) -> Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]:
        key = self.get(key)

        if key is None:
            raise ValueError(
                f"Invalid value {str(key)}. Valid values are {str(self.keys)}"
            )

        return key

    def __or__(self, b) -> Union["Alias", "AliasGroup"]:
        if not isinstance(b, Alias):
            error_message = f"{b} must be type Alias"
            raise TypeError(error_message)

        # value is same between both objects, return new Alias containing union of keys
        if b.value == self.value:
            return Alias(self.value, self.keys | b.keys)

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
        path_group = path_1 | path_2

        # or equivalently (using logical or `|` opporator is recommended):
        # path_group = GroupAlias([path_1, path_2])

        def get_cool_feature(path: Union[int, str]):
            path = path_group[path] # ValueError thrown if invalid path

            url = f"{base_url}/{path}/cool-feature"

            response = requests.get(url)
            return response.json()
    """

    def __init__(self, alias: List[Union[Alias, "AliasGroup"]]) -> None:
        # Instance objects
        self._option_groups = frozenset()
        self._values = frozenset()
        self.option_map = {}

        accepted_types = (Alias, AliasGroup)

        # {alias value: alias object} map
        value_map = {}

        for item in alias:
            # type check for Alias or AliasGroup
            if not isinstance(item, accepted_types):
                error_message = "Items must be type `Alias` or `AliasGroup`"
                raise ValueError(error_message)

            if isinstance(item, AliasGroup):

                # duplicate alias value in AliasGroup get instanced as new Alias
                # containing keys from both parent objects
                for inner_item in item.option_groups:

                    if inner_item.value in value_map:
                        inner_item |= value_map[inner_item.value]

                    value_map[inner_item.value] = inner_item

            else:
                # duplicate alias value in AliasGroup get instanced as new Alias
                # containing keys from both parent objects
                if item.value in value_map:
                    item |= value_map[item.value]

                value_map[item.value] = item

        union, symmetric_difference = frozenset(), frozenset()

        # {value: alias}
        for value, alias_o in value_map.items():
            union |= alias_o.keys
            symmetric_difference ^= alias_o.keys

            # frozenset of Alias value's
            self._values |= {value}

            # frozenset of Alias objects
            self._option_groups |= {alias_o}

            # many to one map of keys to value
            self.option_map.update({keys: alias_o for keys in alias_o.keys})

        duplicate_value = union - symmetric_difference

        if duplicate_value:
            raise ValueError(f"Repeated valid_value {duplicate_value} not allowed")

    def get(
        self, key: Hashable
    ) -> Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]:
        """Get value of Alias in group from a corresponding key, alias value, or
        alias instance. If corresponding Alias value is not present, return None.

        Parameters
        ----------
        value : Hashable
            Valid alias value

        Returns
        -------
        Union[int, float, str, bytes, bool, Callable, tuple, frozenset, None]
           alias value if valid key, value, or Alias instance, else None
        """
        option = self.option_map.get(key)

        if option is None:
            return None

        return option.value

    @property
    def option_groups(self):
        """ Mapping of Alias keys's to Alias value's """
        return self._option_groups

    @property
    def values(self) -> frozenset:
        """ Frozenset of present Alias value's """
        return self._values

    @property
    def keys(self) -> set:
        """ Alias keys """
        return set(self.option_map.keys())

    def __getitem__(self, key):
        option = self.get(key)

        if option is None:
            raise ValueError(
                f"Invalid value {str(key)}. Valid values are {str(self.option_map.keys())}"
            )

        return option

    def __contains__(self, key) -> bool:
        def instance_and_value(k):
            if isinstance(k, Alias):
                return k.value in self.values
            return False

        return key in self.option_map or key in self.values or instance_and_value(key)

    def __or__(self, b) -> "AliasGroup":
        accepted_types = (Alias, AliasGroup)

        if not isinstance(b, accepted_types):
            error_message = f"{b} must be type `Alias` or `AliasGroup`"
            raise TypeError(error_message)

        return AliasGroup([self, b])

    def __str__(self) -> str:
        return str(self.option_groups)

    def __repr__(self) -> str:
        return str(self.option_groups)
