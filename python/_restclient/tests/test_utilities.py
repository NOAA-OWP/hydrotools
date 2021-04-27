#!/usr/bin/env python3

import pytest
from hydrotools._restclient import utilities


@pytest.fixture
def alias_fixture():
    return utilities.Alias("value", "keys")


test_instance_args = [
    ("this", "that"),
    (1, 2),
    (1.0, 2.0),
    (lambda x: x, (1, 2)),
    ((1, 2), "key"),
]


@pytest.mark.parametrize("value,keys", test_instance_args)
def test_instance_alias(value, keys):
    """ Test inputs that can instantiate the class"""
    utilities.Alias(value, keys)


def test_cannot_alter_alias_value(alias_fixture):
    from dataclasses import FrozenInstanceError

    with pytest.raises(FrozenInstanceError):
        alias_fixture.value = "that"


def test_cannot_alter_alias_keys(alias_fixture):
    from dataclasses import FrozenInstanceError

    with pytest.raises(FrozenInstanceError):
        alias_fixture.keys = "that"


def test_pass_mutable_as_keys_then_try_to_change_implicitly_by_ref():
    mute = ["mutable"]
    inst = utilities.Alias("key", mute)

    assert "mutable" in inst

    mute.pop()

    assert "mutable" in inst


def test_get(alias_fixture):
    assert alias_fixture.value == alias_fixture.get("keys")


def test__getitem__(alias_fixture):
    assert alias_fixture.value == alias_fixture["keys"]


def test_get_none(alias_fixture):
    assert alias_fixture.get("None") is None


def test__getitem__raises_value_error(alias_fixture):
    with pytest.raises(ValueError):
        alias_fixture["None"]


@pytest.fixture
def true_false_AG_constructor():
    true = utilities.Alias(True, [True, 1, "true"])
    false = utilities.Alias(False, [False, 0, "false"])

    # ensure instantiation works in both cases
    group = utilities.AliasGroup([true, false])
    assert isinstance(group, utilities.AliasGroup)
    return group


@pytest.fixture
def true_false_AG_using_or():
    true = utilities.Alias(True, [True, 1, "true"])
    false = utilities.Alias(False, [False, 0, "false"])

    group = true | false
    assert isinstance(group, utilities.AliasGroup)
    return group


@pytest.fixture(
    params=["true_false_AG_constructor", "true_false_AG_using_or"], name="group"
)
def true_false_AG_meta_fixture(request):
    """Meta fixture returning multiple AG fixtures.  This is like
    pytest.mark.parametrize, but with fixtures.
    """
    # request is a special pytest fixture that returns context information
    # here, the `getfixturevalue` func is used to get the return value for each
    # fixture passed in `params`
    return request.getfixturevalue(request.param)


def test_if_all_items_in_AliasGroup_not_Alias_should_ValueError():
    true = utilities.Alias(True, [True, 1, "true"])
    false = False

    with pytest.raises(ValueError):
        utilities.AliasGroup([true, false])


def test_raise_ValueError_if_non_scalar_or_callable_in_Alias_constructor():
    with pytest.raises(ValueError):
        utilities.Alias(["should-fail"], "please-fail")


def test_AliasGroup_contains(group):

    assert True in group
    assert False in group

    assert "true" in group
    assert "false" in group

    assert 1 in group
    assert 0 in group


def test_AliasGroup__getitem__(group):

    assert group["true"] is True
    assert group[True] is True
    assert group[1] is True

    assert group["false"] is False
    assert group[False] is False
    assert group[0] is False


def test_AliasGroup_get(group):

    assert group.get("true") is True
    assert group.get(True) is True
    assert group.get(1) is True

    assert group.get("false") is False
    assert group.get(False) is False
    assert group.get(0) is False


def test_build_AliasGroup_with_or_fail_wrong_type():
    true = utilities.Alias(True, [True, 1, "true"])
    false = False

    with pytest.raises(TypeError):
        true | false


def test_Alias_contains():
    true = utilities.Alias(True, "1")
    true_2 = utilities.Alias(True, "2")
    func = utilities.Alias(lambda x: x ** 2, "square")

    assert "1" in true
    assert True in true
    assert true in true

    assert "square" in func
    assert func in func
    x = lambda x: x ** 2
    assert (x in func) == False

    assert true_2 in true
    assert true in true_2

    assert (False in true) == False


def test_reinstantiate_Alias_with_Alias_instance():
    a = utilities.Alias(True, [1, 3])
    assert a.value == True
    assert 2 not in a.keys

    b = utilities.Alias(a, [2])
    assert b.value == True
    assert 2 in b.keys


def test_or_from_same_alias_value():
    a = utilities.Alias(True, [1, 3])
    b = utilities.Alias(True, [2, 2, 1])
    c = a | b

    assert isinstance(c, utilities.Alias)
    assert 3 not in b
    assert 2 not in a

    assert 1 in c
    assert 2 in c
    assert 3 in c


def test_build_AliasGroup_from_same_Alias(group):
    a = utilities.Alias(False, ["False"])

    # build AliasGroup from AliasGroup and Alias
    c = group | a

    assert isinstance(c, utilities.AliasGroup)
    assert "False" in c
    assert "False" not in group


def test_AliasGroup_keys_prop():
    a = utilities.Alias(True, [1, 3])
    b = utilities.Alias(False, [4])
    c = a | b  # AliasGroup

    assert {1, 3, 4}.isdisjoint(c.keys) is False
