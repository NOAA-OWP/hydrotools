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


def test_alias_group():
    true = utilities.Alias(True, [True, 1, "true"])
    false = utilities.Alias(False, [False, 0, "false"])

    assert true.get(True) is True

    group = utilities.AliasGroup([true, false])
    assert group[True] is True
    assert group[1] is True
    assert group["true"] is True

    assert group.get(True) is True
    assert group.get(1) is True
    assert group.get("true") is True

    assert group[False] is False
    assert group[0] is False
    assert group["false"] is False

    assert group.get(False) is False
    assert group.get(0) is False
    assert group.get("false") is False


def test_if_all_items_in_AliasGroup_not_Alias_should_ValueError():
    true = utilities.Alias(True, [True, 1, "true"])
    false = False

    with pytest.raises(ValueError):
        utilities.AliasGroup([true, false])


def test_raise_ValueError_if_non_scalar_or_callable_in_Alias_constructor():
    with pytest.raises(ValueError):
        utilities.Alias(["should-fail"], "please-fail")


def test_build_AliasGroup_with_or():
    true = utilities.Alias(True, [True, 1, "true"])
    false = utilities.Alias(False, [False, 0, "false"])

    group = true | false

    assert isinstance(group, utilities.AliasGroup)


def test_build_AliasGroup_with_or_fail_wrong_type():
    true = utilities.Alias(True, [True, 1, "true"])
    false = False

    with pytest.raises(TypeError):
        group = true | false
