from abc import ABCMeta, abstractmethod

__all__ = ["IterableNonStringLike"]


class IterableNonStringLike(metaclass=ABCMeta):
    """Type iterable that is not a subclass of str or bytes. Useful to test if object
    `isinstance()`.

    Example:
        x = "a-string"
        y = list()
        isinstance(x, IterableNonStringLike) # False
        isinstance(y, IterableNonStringLike) # True
    """

    slots = ()

    @abstractmethod
    def __iter__(self):
        while False:
            yield None

    @classmethod
    def __subclasshook__(cls, C):
        if cls is IterableNonStringLike:
            if any(
                "__iter__" in B.__dict__
                and not issubclass(B, str)
                and not issubclass(B, bytes)
                for B in C.__mro__
            ):
                return True
        return NotImplemented
