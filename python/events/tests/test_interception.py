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

def test_compute_canopy_saturation() -> None:
    """Tests basic functionality of a method to compute the maximum amount of
    canopy interception. Tests whether method correctly raises with bad inputs.
    The method should raise for 0.0 rainfall rate, canopy fraction, or
    evaporation rate."""
    estimate = itc.compute_canopy_saturation(5.0, 0.2, 0.2, 0.3)
    assert np.isclose(estimate, 0.2, atol=0.1)

    # Errors
    with pytest.raises(AssertionError):
        itc.compute_canopy_saturation(0.0, 0.2, 0.2, 0.3)

    with pytest.raises(AssertionError):
        itc.compute_canopy_saturation(5.0, 0.0, 0.2, 0.3)

    with pytest.raises(AssertionError):
        itc.compute_canopy_saturation(5.0, 0.4, 0.2, 0.0)

def test_compute_trunk_saturation() -> None:
    estimate = itc.compute_trunk_saturation(5.0, 0.5, 0.2, 0.3, 0.02, 0.02, 0.02)
    assert np.isclose(estimate, 2.3, atol=0.1)

    # Errors
    with pytest.raises(AssertionError):
        itc.compute_trunk_saturation(0.0, 0.5, 0.2, 0.3, 0.02, 0.02, 0.02)

    with pytest.raises(AssertionError):
        itc.compute_trunk_saturation(5.0, 0.0, 0.2, 0.3, 0.02, 0.02, 0.02)

    with pytest.raises(AssertionError):
        itc.compute_trunk_saturation(5.0, 0.5, 0.2, 0.3, 0.02, 0.0, 0.02)

def test_compute_canopy_loss() -> None:
    estimate = itc.compute_canopy_loss(50.0, 5.0, 0.2, 0.5, 0.3, 0.02)
    assert np.isclose(estimate, 1.5, atol=0.1)

    # Errors
    with pytest.raises(AssertionError):
        itc.compute_canopy_loss(0.0, 5.0, 0.2, 0.5, 0.3, 0.02)

    with pytest.raises(AssertionError):
        itc.compute_canopy_loss(50.0, 0.0, 0.2, 0.5, 0.3, 0.02)

    with pytest.raises(AssertionError):
        itc.compute_canopy_loss(50.0, 5.0, 0.2, 0.0, 0.3, 0.02)

def test_compute_trunk_loss() -> None:
    estimate = itc.compute_trunk_loss(
        5.0, 5.0, 0.2, 0.5, 0.3, 0.02, 0.02, 0.02, 0.2)
    assert np.isclose(estimate, 0.04, atol=0.01)

    # Errors
    with pytest.raises(AssertionError):
        itc.compute_trunk_loss(
            0.0, 5.0, 0.2, 0.5, 0.3, 0.02, 0.02, 0.02, 0.2)
        
    with pytest.raises(AssertionError):
        itc.compute_trunk_loss(
            5.0, 0.0, 0.2, 0.5, 0.3, 0.02, 0.02, 0.02, 0.2)
        
    with pytest.raises(AssertionError):
        itc.compute_trunk_loss(
            5.0, 5.0, 0.2, 0.0, 0.3, 0.02, 0.02, 0.02, 0.2)
