"""Test request partitioning methods."""
import pytest
from hydrotools.waterdata_client.request_partitioning import group_string_iterable

@pytest.mark.parametrize("test_case, expected", [
    ([f"item-{i}" for i in range(5)], ("item-0,item-1,item-2", "item-3,item-4"))
])
def test_default_string_iterable_grouping(test_case, expected):
    """Tests string iterable group method."""
    assert group_string_iterable(test_case) == expected

@pytest.mark.parametrize("test_case, size, expected", [
    ([f"item-{i}" for i in range(5)], 2, ("item-0,item-1", "item-2,item-3", "item-4"))
])
def test_chunk_size_string_iterable_grouping(test_case, size, expected):
    """Tests string iterable group method."""
    assert group_string_iterable(test_case, group_size=size) == expected

@pytest.mark.parametrize("test_case, delimiter, expected", [
    ([f"item-{i}" for i in range(5)], ":", ("item-0:item-1:item-2", "item-3:item-4"))
])
def test_delimiter_string_iterable_grouping(test_case, delimiter, expected):
    """Tests string iterable group method."""
    assert group_string_iterable(test_case, delimiter=delimiter) == expected
