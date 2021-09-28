#!/usr/bin/env python3

import pytest
from hydrotools.nwm_client import utils

crosswalk_test_cases = [
    ({"usgs_site_codes": "02465292"}, [18206880]),
    ({"usgs_site_codes": "02465292,04234000"}, [18206880, 21983115]),
    ({"usgs_site_codes": ["02465292", "04234000"]}, [18206880, 21983115]),
    ({"nwm_feature_ids": [18206880]}, ["02465292"]),
    ({"nwm_feature_ids": [18206880, 21983115]}, ["02465292", "04234000"]),
    ({"nwm_feature_ids": [18206880, 21983115]}, ["02465292", "04234000"]),
]


@pytest.mark.parametrize("test,valid", crosswalk_test_cases)
def test_crosswalk(test, valid):
    key = [list(test.keys())[0][:-1]]
    res = utils.crosswalk(**test)
    assert res[res.columns.difference(key)].isin(valid).all().bool()
