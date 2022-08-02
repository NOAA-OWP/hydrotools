import pint
from dataclasses import dataclass
import numpy.typing as npt
import pandas as pd
import sys

def _default_registry() -> pint.UnitRegistry:
    """Get a default registry depending upon Python version."""
    version = sys.version_info.major + sys.version_info.minor/10.0
    if version < 3.8:
        return pint.UnitRegistry()
    return pint.UnitRegistry(cache_folder=":auto:")

@dataclass
class UnitHandler:
    """Engine to handle unit of measurement conversions.

    Attributes
    ----------
    unit_registry: pint.UnitRegistry, default pint.UnitRegistry(cache_folder=":auto:")
        pint.UnitRegistry that handles all units used by UnitHandler.
    
    """
    unit_registry: pint.UnitRegistry = _default_registry()

    def conversion_factor(self, from_units: str, to_units: str) -> float:
        """Compute and return a conversion factor from from_units to 
        to_units.
        
        Parameters
        ----------
        from_units: pint.UnitRegistry.Quantity compatible str
            Units from which to convert (e.g. "m^3/s")
        to_units: pint.UnitRegistry.Quantity compatible str
            Desired conversion units (e.g. "ft^3/s")
            
        Returns
        -------
        result: float
            Conversion factor to transform from_units to to_units.

        Example
        -------
        >>> unit_handler = UnitHandler.UnitHandler()
        >>> unit_handler.conversion_factor("ft", "m")
        0.30479999999999996
        """
        # Return conversion factor
        return self.unit_registry.Quantity(1, from_units).to(to_units).magnitude

    def convert_values(self, value: npt.ArrayLike, from_units: str, to_units: str) -> npt.ArrayLike:
        """Convert value from from_units to to_units.
        
        Parameters
        ----------
        value: array-like, required
            Values to convert.
        from_units: pint.UnitRegistry.Quantity compatible str
            Units from which to convert (e.g. "m^3/s")
        to_units: pint.UnitRegistry.Quantity compatible str
            Desired conversion units (e.g. "ft^3/s")
            
        Returns
        -------
        result: array-like
            Converted values same shape as value.

        Example
        -------
        >>> unit_handler = UnitHandler.UnitHandler()
        >>> unit_handler.convert_values([1, 1, 1], "ft", "m")
        array([0.3048, 0.3048, 0.3048])
        """
        # Check for pandas.series
        if isinstance(value, pd.Series):
            return self.unit_registry.Quantity(value.values, from_units).to(to_units).magnitude

        # Return converted value
        return self.unit_registry.Quantity(value, from_units).to(to_units).magnitude
