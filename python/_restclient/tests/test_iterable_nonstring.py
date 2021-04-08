#!/usr/bin/env python3

import pytest
from hydrotools._restclient import _iterable_nonstring


class FalseMock(str):
    a = "false_mock"

    def __iter__(self):
        for c in self.a:
            yield c


false_string_args = [
    "should fail",
    b"should fail bytes",
    str("should fail"),
    FalseMock(),
]


@pytest.mark.parametrize("arg", false_string_args)
def test_strings_are_false(arg):
    assert isinstance(arg, _iterable_nonstring.IterableNonStringLike) is False


class TrueMock:
    a = [1, 2, 3]

    def __iter__(self):
        for x in self.a:
            yield x


true_args = [list(), dict(), set(), frozenset(), TrueMock()]


@pytest.mark.parametrize("arg", true_args)
def test_true_collection_types(arg):
    assert isinstance(arg, _iterable_nonstring.IterableNonStringLike) is True
