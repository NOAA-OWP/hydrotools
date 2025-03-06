"""Tests functionality of the interception module."""
import pytest
import hydrotools.events.models.interception as itc
import numpy as np

def test_compute_interception() -> None:
    """Tests basic functionality of top level method of interception module.
    Also tests that the method correctly raises with bad inputs. Specifically,
    if the gross rainfall, average rainfall rate, or canopy fraction is 0.0,
    the method should raise an AssertionError."""
    estimate = itc.compute_interception(50.0, 5.0, 0.5)
    assert np.isclose(estimate, 2.5, atol=0.1)

    # Errors
    with pytest.raises(AssertionError):
        itc.compute_interception(0.0, 5.0, 0.5)
        
    with pytest.raises(AssertionError):
        itc.compute_interception(50.0, 0.0, 0.5)

    with pytest.raises(AssertionError):
        itc.compute_interception(50.0, 5.0, 0.0)

def test_compute_canopy_interception() -> None:
    estimate = itc.compute_canopy_saturation(5.0, 0.2, 0.2, 0.3)
    assert np.isclose(estimate, 0.2, atol=0.1)

    # Errors
    # _ = itc.compute_canopy_saturation(0.0, 0.2, 0.2, 0.3)
    # _ = itc.compute_canopy_saturation(5.0, 0.0, 0.2, 0.3)
    # _ = itc.compute_canopy_saturation(5.0, 0.4, 0.2, 0.0)

    estimate = itc.compute_trunk_saturation(5.0, 0.5, 0.2, 0.3, 0.02, 0.02, 0.02)
    assert np.isclose(estimate, 2.3, atol=0.1)

    # Errors
    # _ = itc.compute_trunk_saturation(0.0, 0.5, 0.2, 0.3, 0.02, 0.02, 0.02)
    # _ = itc.compute_trunk_saturation(5.0, 0.0, 0.2, 0.3, 0.02, 0.02, 0.02)
    # _ = itc.compute_trunk_saturation(5.0, 0.5, 0.2, 0.3, 0.02, 0.0, 0.02)

    estimate = itc.compute_canopy_loss(50.0, 5.0, 0.2, 0.5, 0.3, 0.02)
    assert np.isclose(estimate, 1.5, atol=0.1)

    # Errors
    # _ = itc.compute_canopy_loss(0.0, 5.0, 0.2, 0.5, 0.3, 0.02)
    # _ = itc.compute_canopy_loss(50.0, 0.0, 0.2, 0.5, 0.3, 0.02)
    # _ = itc.compute_canopy_loss(50.0, 5.0, 0.2, 0.0, 0.3, 0.02)

    estimate = itc.compute_trunk_loss(
        5.0, 5.0, 0.2, 0.5, 0.3, 0.02, 0.02, 0.02, 0.2)
    assert np.isclose(estimate, 0.04, atol=0.01)

    # Errors
    # _ = itc.compute_trunk_loss(
    #     0.0, 5.0, 0.2, 0.5, 0.3, 0.02, 0.02, 0.02, 0.2)
    # _ = itc.compute_trunk_loss(
    #     5.0, 0.0, 0.2, 0.5, 0.3, 0.02, 0.02, 0.02, 0.2)
    # _ = itc.compute_trunk_loss(
    #     5.0, 5.0, 0.2, 0.0, 0.3, 0.02, 0.02, 0.02, 0.2)
