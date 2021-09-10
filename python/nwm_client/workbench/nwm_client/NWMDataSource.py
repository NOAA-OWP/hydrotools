"""
===============
NWM Data Source
===============
Tools for discovering operational NWM NetCDF data.

Classes
-------
NWMDataSource
HTTPDataSource
GCPDataSource
"""
from abc import ABC, abstractmethod

class NWMDataSource(ABC):

    @abstractmethod
    def query(self):
        """Abstract method to query for NWM data."""

class HTTPDataSource(NWMDataSource):

    def query(self):
        """Query for NWM data from generic web servers."""

class GCPDataSource(NWMDataSource):

    def query(self):
        """Query for NWM data on Google Cloud Platform."""
