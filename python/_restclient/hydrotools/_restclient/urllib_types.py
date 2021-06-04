from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Callable
import urllib.parse as parse

__all__ = ["Quote"]

# descriptive sentinel value used by Url constructor `quote_treatment` kwarg to desert
# between a true default of value vs a non-default value (Quote enum)
QUOTE_PLUS_OR_CARRY = object()

# descriptive sentienl value used by Url `safe` kwarg for distinction.
# default value is "/"
FORWARD_SLASH = object()


@dataclass(frozen=True)
class QuoteStyle:
    quote_style: Callable
    unquote_style: Callable


class Quote(Enum):
    """ Enumeration of quote/unquote handling methods. """

    QUOTE = QuoteStyle(quote_style=parse.quote, unquote_style=parse.unquote)
    QUOTE_PLUS = QuoteStyle(
        quote_style=parse.quote_plus, unquote_style=parse.unquote_plus
    )
    QUOTE_FROM_BYTES = QuoteStyle(
        quote_style=parse.quote_from_bytes,
        unquote_style=parse.unquote_to_bytes,
    )

    def quote(self, *args, **kwargs):
        return self.value.quote_style(*args, **kwargs)

    def unquote(self, *args, **kwargs):
        return self.value.unquote_style(*args, **kwargs)

    @property
    def quote_style(self):
        return self.value.quote_style

    @property
    def unquote_style(self):
        return self.value.unquote_style
