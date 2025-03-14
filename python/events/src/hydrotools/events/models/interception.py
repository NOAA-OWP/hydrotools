"""
============
Interception
============

Methods to support the estimation of rainfall interception for a single event
across a single catchment. These methods implement the Gash model of canopy
interception adjusted for a single storm using reasonable defaults from
Miralles et al, 2010. The primary method in this module is
`compute_interception`. Use this method to estimate intercepted rainfall on
an event basis using default parameters from the literature.
`compute_interception` will call the neccessary support methods in the
appropriate order to estimate canopy interception per Gash (1979).

Gash, J. H. C. (1979). An analytical model of rainfall interception by forests.
    Quarterly Journal of the Royal Meteorological Society, 105(443), 43-55.
Miralles, D. G., Gash, J. H., Holmes, T. R. H., De Jeu, R. A. M., & Dolman,
    A. J. (2010). Global canopy interception from satellite observations.
    Journal of Geophysical Research: Atmospheres, 115(D16), 2009JD013530.
    https://doi.org/10.1029/2009JD013530
Valente, F., David, J. S., & Gash, J. H. C. (1997). Modelling interception loss
    for two sparse eucalypt and pine forests in central Portugal using
    reformulated Rutter and Gash analytical models. Journal of hydrology,
    190(1-2), 141-162.

Functions
---------
compute_canopy_saturation
compute_trunk_saturation
compute_canopy_loss
compute_trunk_loss
compute_interception

Classes
-------
DefaultParameters
"""

from dataclasses import dataclass
import warnings
import numpy as np

@dataclass
class DefaultParameters:
    """
    Dataclass used to store module level default parameters.

    Parameters
    ----------
    canopy_storage: float, optional, default 1.2
        Minimum depth of water required to saturate the canopy. Typically 1.2
        mm (Miralles et al, 2010). Notated $S_c$. Expected to vary little by
        location and leaf type (± 0.4 mm, standard deviation). Measurement
        units should correspond to rainfall_rate (i.e. if rainfall_rate is in
        mm/hour, then canopy_storage should be in mm).
    evaporation_rate: float, optional, default 0.3
        Average evaporation rate. Typically 0.3 mm/hour (Miralles et al, 2010).
        Notated $E_c$. Expected to vary little between locations
        (± 0.1 mm/hour, standard deviation). Should be in the same measurement
        units as rainfall_rate.
    trunk_fraction: float, optional, default 0.02
        Fraction of rainfall hitting the "trunks" under the canopy. Typically
        0.02 (Miralles et al, 2010). Notated $p_d$. Unitless.
    trunk_evaporation: float, optional, default 0.02
        Fraction of evaporation originating from vegetation "trunks." Typically
        0.02 (Miralles et al, 2010). Notated $\\epsilon$. Unitless.
    trunk_capacity: float, optional, default 0.02
        Minimum depth of water required to saturate trunks under the canopy.
        Typically 0.02 mm (Miralles et al, 2010). Notated $S_t$. Measurement
        units should correspond to rainfall_rate (i.e. if rainfall_rate is in
        mm/hour, then trunk_capacity should be in mm).
    """
    canopy_storage: float = 1.2
    evaporation_rate: float = 0.3
    trunk_fraction: float = 0.02
    trunk_evaporation: float = 0.02
    trunk_capacity: float = 0.02

_DEFAULT_PARAMETERS: DefaultParameters = DefaultParameters()
"""Module level default parameters."""

def compute_canopy_saturation(
        rainfall_rate: float,
        canopy_storage: float,
        trunk_evaporation: float = _DEFAULT_PARAMETERS.trunk_evaporation,
        evaporation_rate: float = _DEFAULT_PARAMETERS.evaporation_rate
) -> float:
    """
    Compute the amount of rainfall necessary to saturate the canopy.
    Notated as $P_g'$ in Miralles et al, 2010. Typically in mm.

    Parameters
    ----------
    rainfall_rate: float, required
        Mean rainfall rate in L/T, typically mm/hour. Notated 'R'.
    canopy_storage: float, required
        Minimum depth of water required to saturate the canopy. Typically 1.2
        mm (Miralles et al, 2010). Notated $S_c$. Expected to vary little by
        location and leaf type (± 0.4 mm, standard deviation). Measurement
        units should correspond to rainfall_rate (i.e. if rainfall_rate is in
        mm/hour, then canopy_storage should be in mm).
    evaporation_rate: float, optional, default 0.3
        Average evaporation rate. Typically 0.3 mm/hour (Miralles et al, 2010).
        Notated $E_c$. Expected to vary little between locations
        (± 0.1 mm/hour, standard deviation). Should be in the same measurement
        units as rainfall_rate.
    trunk_evaporation: float, optional, default 0.02
        Fraction of evaporation originating from vegetation "trunks." Typically
        0.02 (Miralles et al, 2010). Notated $\\epsilon$. Unitless.

    Returns
    -------
    Maximum canopy storage (L) as a float.

    Raises
    ------
    AssertionError
        If rainfall_rate, canopy_storage, or evaporation_rate are not > 0. If
        trunk_evaporation is not >= 0 and < 1.0. This is true only if python
        optimization is not enabled.
    """
    # Validate
    assert rainfall_rate > 0, "rainfall rate must be a number > 0"
    assert canopy_storage > 0, "canopy storage must be a number > 0"
    assert evaporation_rate > 0, "evaporation rate must be a number > 0"
    assert 0.0 <= trunk_evaporation < 1.0, \
        "trunk evaporation range is [0.0, 1.0)"
    if evaporation_rate >= rainfall_rate:
        message = "evaporation rate >= rainfall rate, use result with caution"
        warnings.warn(message, UserWarning)

    return (-((rainfall_rate * canopy_storage) /
        ((1-trunk_evaporation) * evaporation_rate)) *
        np.log(1-((1-trunk_evaporation)*evaporation_rate/rainfall_rate)))

def compute_trunk_saturation(
        rainfall_rate: float,
        canopy_fraction: float,
        canopy_saturation: float,
        evaporation_rate: float = _DEFAULT_PARAMETERS.evaporation_rate,
        trunk_capacity: float = _DEFAULT_PARAMETERS.trunk_capacity,
        trunk_fraction: float = _DEFAULT_PARAMETERS.trunk_fraction,
        trunk_evaporation: float = _DEFAULT_PARAMETERS.trunk_evaporation
) -> float:
    """
    Compute the amount of rainfall necessary to saturate the trunks under
    the canopy. Notated as $P_g''$ in Miralles et al, 2010. Typically in mm.

    Parameters
    ----------
    rainfall_rate: float, required
        Mean rainfall rate in L/T, typically mm/hour. Notated 'R'.
    canopy_fraction: float, required
        Projected portion of canopy cover, unitless. Notated 'c'. Valid
        range is (0.0, 1.0]
    canopy_saturation: float, required
        Maximum canopy storage, typically mm. Notated $P_g'$. Can be computed
        using `compute_canopy_saturation`.
    evaporation_rate: float, optional, default 0.3
        Average evaporation rate. Typically 0.3 mm/hour (Miralles et al, 2010).
        Notated $E_c$. Expected to vary little between locations
        (± 0.1 mm/hour, standard deviation). Should be in the same measurement
        units as rainfall_rate.
    trunk_fraction: float, optional, default 0.02
        Fraction of rainfall hitting the "trunks" under the canopy. Typically
        0.02 (Miralles et al, 2010). Notated $p_d$. Unitless.
    trunk_evaporation: float, optional, default 0.02
        Fraction of evaporation originating from vegetation "trunks." Typically
        0.02 (Miralles et al, 2010). Notated $\\epsilon$. Unitless.
    trunk_capacity: float, optional, default 0.02
        Minimum depth of water required to saturate trunks under the canopy.
        Typically 0.02 mm (Miralles et al, 2010). Notated $S_t$. Measurement
        units should correspond to rainfall_rate (i.e. if rainfall_rate is in
        mm/hour, then trunk_capacity should be in mm).

    Returns
    -------
    Maximum trunk storage (L) as a float.

    Raises
    ------
    AssertionError
        If rainfall_rate, canopy_storage, or evaporation_rate are not > 0. If
        trunk_evaporation, trunk_fraction, or canopy_fraction are not >= 0 and 
        < 1.0. This is true only if python optimization is not enabled.
    """
    # Validate
    assert rainfall_rate > 0, "rainfall rate must be a number > 0"
    assert 0.0 <= trunk_evaporation < 1.0, \
        "trunk evaporation range is [0.0, 1.0)"
    assert 0.0 < trunk_fraction <= 1.0, \
        "trunk fraction range is (0.0, 1.0]"
    assert 0.0 < canopy_fraction <= 1.0, \
        "canopy fraction range is (0.0, 1.0]"
    if evaporation_rate >= rainfall_rate:
        message = "evaporation rate >= rainfall rate, use result with caution"
        warnings.warn(message, UserWarning)

    return canopy_saturation + (rainfall_rate * trunk_capacity /
        (trunk_fraction * canopy_fraction *
         (rainfall_rate - evaporation_rate*(1-trunk_evaporation))))

def compute_canopy_loss(
        gross_rainfall: float,
        rainfall_rate: float,
        canopy_saturation: float,
        canopy_fraction: float,
        evaporation_rate: float = _DEFAULT_PARAMETERS.evaporation_rate,
        trunk_evaporation: float = _DEFAULT_PARAMETERS.trunk_evaporation
) -> float:
    """
    Compute the amount of canopy intercepted rainfall. Typically in mm.

    Parameters
    ----------
    gross_rainfall: float, required
        Storm total rainfall, typically in mm. Notated $P_g$.
    rainfall_rate: float, required
        Mean rainfall rate in L/T, typically mm/hour. Notated 'R'.
    canopy_saturation: float, required
        Maximum canopy storage, typically mm. Notated $P_g'$. Can be computed
        using `compute_canopy_saturation`.
    canopy_fraction: float, required
        Projected portion of canopy cover, unitless. Notated 'c'. Valid
        range is (0.0, 1.0]
    evaporation_rate: float, optional, default 0.3
        Average evaporation rate. Typically 0.3 mm/hour (Miralles et al, 2010).
        Notated $E_c$. Expected to vary little between locations
        (± 0.1 mm/hour, standard deviation). Should be in the same measurement
        units as rainfall_rate.
    trunk_evaporation: float, optional, default 0.02
        Fraction of evaporation originating from vegetation "trunks." Typically
        0.02 (Miralles et al, 2010). Notated $\\epsilon$. Unitless.

    Returns
    -------
    Depth of canopy intercepted rainfall (L) as a float.

    Raises
    ------
    AssertionError
        If gross_rainfall or rainfall_rate are not > 0. If
        canopy_fraction is not > 0 and <= 1.0. This is true only if python
        optimization is not enabled.
    """
    # Validate
    assert gross_rainfall > 0, "gross rainfall must be a number > 0"
    assert rainfall_rate > 0, "rainfall rate must be a number > 0"
    assert 0.0 < canopy_fraction <= 1.0, \
        "canopy fraction range is (0.0, 1.0]"
    if evaporation_rate >= rainfall_rate:
        message = "evaporation rate >= rainfall rate, use result with caution"
        warnings.warn(message, UserWarning)

    if gross_rainfall <= canopy_saturation:
        return canopy_fraction * gross_rainfall

    return canopy_fraction * (canopy_saturation +
        ((1-trunk_evaporation)*evaporation_rate/rainfall_rate)*
        (gross_rainfall-canopy_saturation))

def compute_trunk_loss(
        gross_rainfall: float,
        rainfall_rate: float,
        canopy_saturation: float,
        canopy_fraction: float,
        trunk_saturation: float,
        evaporation_rate: float = _DEFAULT_PARAMETERS.evaporation_rate,
        trunk_capacity: float = _DEFAULT_PARAMETERS.trunk_capacity,
        trunk_fraction: float = _DEFAULT_PARAMETERS.trunk_fraction,
        trunk_evaporation: float = _DEFAULT_PARAMETERS.trunk_evaporation
) -> float:
    """
    Compute the amount of trunk intercepted rainfall. Typically in mm.

    Parameters
    ----------
    gross_rainfall: float, required
        Storm total rainfall, typically in mm. Notated $P_g$.
    rainfall_rate: float, required
        Mean rainfall rate in L/T, typically mm/hour. Notated 'R'.
    canopy_saturation: float, required
        Maximum canopy storage, typically mm. Notated $P_g'$. Can be computed
        using `compute_canopy_saturation`.
    canopy_fraction: float, required
        Projected portion of canopy cover, unitless. Notated 'c'. Valid
        range is (0.0, 1.0]
    trunk_saturation: float, required
        Maximum trunk storage, typically mm. Notated $P_g''$. Can be computed
        using `compute_trunk_saturation`.
    evaporation_rate: float, optional, default 0.3
        Average evaporation rate. Typically 0.3 mm/hour (Miralles et al, 2010).
        Notated $E_c$. Expected to vary little between locations
        (± 0.1 mm/hour, standard deviation). Should be in the same measurement
        units as rainfall_rate.
    trunk_fraction: float, optional, default 0.02
        Fraction of rainfall hitting the "trunks" under the canopy. Typically
        0.02 (Miralles et al, 2010). Notated $p_d$. Unitless.
    trunk_evaporation: float, optional, default 0.02
        Fraction of evaporation originating from vegetation "trunks." Typically
        0.02 (Miralles et al, 2010). Notated $\\epsilon$. Unitless.
    trunk_capacity: float, optional, default 0.02
        Minimum depth of water required to saturate trunks under the canopy.
        Typically 0.02 mm (Miralles et al, 2010). Notated $S_t$. Measurement
        units should correspond to rainfall_rate (i.e. if rainfall_rate is in
        mm/hour, then trunk_capacity should be in mm).

    Returns
    -------
    Depth of canopy intercepted rainfall (L) as a float.

    Raises
    ------
    AssertionError
        If gross_rainfall or rainfall_rate are not > 0. If
        canopy_fraction is not > 0 and <= 1.0. This is true only if python
        optimization is not enabled.
    """
    # Validate
    assert gross_rainfall > 0, "gross rainfall must be a number > 0"
    assert rainfall_rate > 0, "rainfall rate must be a number > 0"
    assert 0.0 < canopy_fraction <= 1.0, \
        "canopy fraction range is (0.0, 1.0]"
    if evaporation_rate >= rainfall_rate:
        message = "evaporation rate >= rainfall rate, use result with caution"
        warnings.warn(message, UserWarning)

    if gross_rainfall <= trunk_saturation:
        return trunk_capacity

    return (trunk_fraction * canopy_fraction *
        (1-(1-trunk_evaporation)*evaporation_rate/rainfall_rate)*
        (gross_rainfall-canopy_saturation))

def compute_interception(
        gross_rainfall: float,
        rainfall_rate: float,
        canopy_fraction: float,
        canopy_storage: float = _DEFAULT_PARAMETERS.canopy_storage,
        evaporation_rate: float = _DEFAULT_PARAMETERS.evaporation_rate,
        trunk_fraction: float = _DEFAULT_PARAMETERS.trunk_fraction,
        trunk_evaporation: float = _DEFAULT_PARAMETERS.trunk_evaporation,
        trunk_capacity: float = _DEFAULT_PARAMETERS.trunk_capacity
) -> float:
    """
    Compute the amount of total intercepted rainfall. Typically in mm.

    Parameters
    ----------
    gross_rainfall: float, required
        Storm total rainfall, typically in mm. Notated $P_g$.
    rainfall_rate: float, required
        Mean rainfall rate in L/T, typically mm/hour. Notated 'R'.
    canopy_fraction: float, required
        Projected portion of canopy cover, unitless. Notated 'c'. Valid
        range is (0.0, 1.0]
    canopy_storage: float, optional, default 1.2
        Minimum depth of water required to saturate the canopy. Typically 1.2
        mm (Miralles et al, 2010). Notated $S_c$. Expected to vary little by
        location and leaf type (± 0.4 mm, standard deviation). Measurement
        units should correspond to rainfall_rate (i.e. if rainfall_rate is in
        mm/hour, then canopy_storage should be in mm).
    evaporation_rate: float, optional, default 0.3
        Average evaporation rate. Typically 0.3 mm/hour (Miralles et al, 2010).
        Notated $E_c$. Expected to vary little between locations
        (± 0.1 mm/hour, standard deviation). Should be in the same measurement
        units as rainfall_rate.
    trunk_fraction: float, optional, default 0.02
        Fraction of rainfall hitting the "trunks" under the canopy. Typically
        0.02 (Miralles et al, 2010). Notated $p_d$. Unitless.
    trunk_evaporation: float, optional, default 0.02
        Fraction of evaporation originating from vegetation "trunks." Typically
        0.02 (Miralles et al, 2010). Notated $\\epsilon$. Unitless.
    trunk_capacity: float, optional, default 0.02
        Minimum depth of water required to saturate trunks under the canopy.
        Typically 0.02 mm (Miralles et al, 2010). Notated $S_t$. Measurement
        units should correspond to rainfall_rate (i.e. if rainfall_rate is in
        mm/hour, then trunk_capacity should be in mm).

    Returns
    -------
    Depth of canopy intercepted rainfall (L) as a float.

    Raises
    ------
    AssertionError
        If gross_rainfall, evaporation_rate, or rainfall_rate are not > 0. If
        canopy_fraction is not > 0 and <= 1.0. This is true only if python
        optimization is not enabled.
    """
    # Validate
    assert gross_rainfall > 0, "gross rainfall must be a number > 0"
    assert rainfall_rate > 0, "rainfall rate must be a number > 0"
    assert evaporation_rate > 0, "rainfall rate must be a number > 0"
    assert 0.0 < canopy_fraction <= 1.0, \
        "canopy fraction range is (0.0, 1.0]"
    if evaporation_rate >= rainfall_rate:
        message = "evaporation rate >= rainfall rate, use result with caution"
        warnings.warn(message, UserWarning)

    # Maximum canopy saturation
    canopy_saturation = compute_canopy_saturation(
        rainfall_rate,
        canopy_storage,
        trunk_evaporation,
        evaporation_rate
    )

    # Maximum trunk saturation
    trunk_saturation = compute_trunk_saturation(
        rainfall_rate,
        canopy_fraction,
        canopy_saturation,
        evaporation_rate,
        trunk_capacity,
        trunk_fraction,
        trunk_evaporation
    )

    # Interception loss from canopy (mm)
    canopy_loss = compute_canopy_loss(
        gross_rainfall,
        rainfall_rate,
        canopy_saturation,
        canopy_fraction,
        evaporation_rate,
        trunk_evaporation
    )

    # Interception loss from trunks (mm)
    trunk_loss = compute_trunk_loss(
        gross_rainfall,
        rainfall_rate,
        canopy_saturation,
        canopy_fraction,
        trunk_saturation,
        evaporation_rate,
        trunk_capacity,
        trunk_fraction,
        trunk_evaporation
    )

    # Compute total loss
    total_loss = canopy_loss + trunk_loss
    if total_loss < gross_rainfall:
        return total_loss
    return gross_rainfall
