import pytest
from functools import partial


# local imports
from hydrotools.nwis_client._utilities import (
    get_varkeyword_arg,
    verify_case_insensitive_kwargs,
)


def test_get_varkeyword_arg():
    def foo(**kwargs) -> None:
        ...

    assert get_varkeyword_arg(foo) == "kwargs"


def test_get_varkeyword_arg_without_kwargs():
    def foo(a: int) -> None:
        ...

    assert get_varkeyword_arg(foo) == None


def test_verify_case_insensitive_kwargs_warns():
    @verify_case_insensitive_kwargs
    def foo(a: int, **kwargs) -> int:
        return a

    with pytest.warns(RuntimeWarning, match="function parameter, 'a', provided as 'A'"):
        input = 12
        res = foo(a=input, A=12)
        assert res == input


def test_verify_case_insensitive_kwargs():
    @verify_case_insensitive_kwargs
    def foo(a: int) -> int:
        return a

    assert foo(a=12) == 12


def test_verify_case_insensitive_kwargs_raises():
    def raiser(e: Exception, s: str = None):
        if s:
            raise e(s)
        raise e

    @verify_case_insensitive_kwargs(handler=partial(raiser, TypeError))
    def foo(a: int, **kwargs) -> int:
        return a

    with pytest.raises(TypeError, match="function parameter, 'a', provided as 'A'"):
        foo(a=12, A=12)
