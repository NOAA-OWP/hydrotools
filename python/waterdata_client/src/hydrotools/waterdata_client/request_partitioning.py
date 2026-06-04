"""Methods to support request partitioning for arguments that accept Sequence."""
import sys
from typing import Iterable, TypeAlias, Annotated
from pydantic import BeforeValidator

if sys.version_info >= (3, 12):
    from itertools import batched
else:
    # Define roughly equivalent function for batched
    from itertools import islice
    from typing import TypeVar, Generator

    T = TypeVar("T")

    def batched(
            iterable: Iterable[T],
            n: int,
            strict: bool = False
        ) -> Generator[tuple[T, ...], None, None]:
        """Batch data from the iterable into tuples of length n. The last batch may
        be shorter than n. If strict is true, will raise a ValueError if the final
        batch is shorter than n. Loops over the input iterable and accumulates data
        into tuples up to size n. The input is consumed lazily, just enough to fill
        a batch. The result is yielded as soon as the batch is full or when the
        input iterable is exhausted.
        """
        if n < 1:
            raise ValueError("n must be at least one")
        iterator = iter(iterable)
        while batch := tuple(islice(iterator, n)):
            if strict and len(batch) != n:
                raise ValueError("batched(): incomplete batch")
            yield batch

def group_string_iterable(
        iterable: Iterable[str],
        group_size: int = 3,
        delimiter: str = ","
) -> tuple[str, ...]:
    """Takes an iterable of strings and returns a grouped tuple of strings. Resulting
    strings are delimited groups of group_size.
    
    Args:
        iterable: Input iterable of strings to group.
        group_size: The number of strings to group together.
        delimiter: How component strings are separated in each grouped string.
    
    Returns:
        Tuple of grouped strings.

    Example:
        >>> group_string_iterable(['item-0', 'item-1', 'item-2', 'item-3', 'item-4'], 2)
        ('item-0,item-1', 'item-2,item-3', 'item-4')
    """
    return tuple(delimiter.join(b) for b in batched(iterable, group_size))

def validate_sequence_argument(
        iterable_object: str | Iterable[str]
) -> list[str]:
    """Reusable validator for string iterable arguments."""
    # Plain strings are put into a list
    if isinstance(iterable_object, str):
        return [iterable_object]

    # Iterables are converted to lists
    if isinstance(iterable_object, Iterable):
        if all(isinstance(s, str) for s in iterable_object):
            return list(iterable_object)
    raise ValueError(f"Unable to convert {iterable_object} to list[str]")

StringList: TypeAlias = Annotated[
    list[str],
    BeforeValidator(validate_sequence_argument)
]
"""Annotated type that validates and converts object to list of strings.
"""
