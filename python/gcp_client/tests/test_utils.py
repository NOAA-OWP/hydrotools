#!/usr/bin/env python3

import pytest
from evaluation_tools.gcp_client import utils

crosswalk_test_cases = [
    ("02465292", [18206880]),
    ("02465292,04234000", [18206880, 21983115]),
    (["02465292", "04234000"], [18206880, 21983115]),
]


@pytest.mark.parametrize("test,valid", crosswalk_test_cases)
def test_crosswalk(test, valid):
    assert utils.crosswalk(test)["nwm_feature_id"].isin(valid).all()
