import pytest
from hydrotools.metrics import metrics

import pandas as pd

all_tp_case = pd.DataFrame({
    "obs": pd.Categorical([True, True, True]),
    "sim": pd.Categorical([True, True, True])
})
all_fp_case = pd.DataFrame({
    "obs": pd.Categorical([False, False, False]),
    "sim": pd.Categorical([True, True, True])
})
all_fn_case = pd.DataFrame({
    "obs": pd.Categorical([True, True, True]),
    "sim": pd.Categorical([False, False, False])
})
all_tn_case = pd.DataFrame({
    "obs": pd.Categorical([False, False, False]),
    "sim": pd.Categorical([False, False, False])
})

scenarios = [
    (all_tp_case, "true_positive", 3),
    (all_fp_case, "false_positive", 3),
    (all_fn_case, "false_negative", 3),
    (all_tn_case, "true_negative", 3)
]

@pytest.mark.parametrize("data,check,value", scenarios)
def test_compute_contingency_table_scenarios(data, check, value):
    # Construct contingency table
    with pytest.warns(UserWarning):
        table = metrics.compute_contingency_table(data["obs"], data["sim"])

    # Validate correct values
    for component, val in table.items():
        if component == check:
            assert val == value
        else:
            assert val == 0
