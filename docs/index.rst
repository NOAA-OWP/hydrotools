``HydroTools``
=====================

Tools for retrieving hydrological data

.. toctree::
   :hidden:
   :maxdepth: 2

   examples

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: API:

   hydrotools.nwis_client
   hydrotools.gcp_client
   hydrotools._restclient
   hydrotools.metrics
   hydrotools.events.event_detection


Motivation
----------

We developed hydrotools with data scientists in mind. We attempted
to ensure the simplest methods such as ``get`` both accepted and
returned data structures frequently used by data scientists using
scientific Python. Specifically, this means that
|pandas.DataFrames|_,
|geopandas.GeoDataFrames|_,
and
|numpy.arrays|_
are the most frequently encountered data structures when using
hydrotools. The majority of methods include sensible defaults that
cover the majority of use-cases, but allow customization if required.

We also attempted to adhere to organizational (NOAA-OWP) data standards
where they exist. This means ``pandas.DataFrames`` will contain column
labels like ``usgs_site_code``, ``start_date``, ``value_date``, and
``measurement_unit`` which are consistent with organization wide naming
conventions. Our intent is to make retrieving, evaluating, and exporting
data as easy and reproducible as possible for scientists, practitioners
and other hydrological experts.

.. |numpy.arrays| replace:: ``numpy.arrays``
.. _numpy.arrays: https://numpy.org/doc/stable/reference/arrays.html#array-objects
.. |geopandas.GeoDataFrames| replace:: ``geopandas.GeoDataFrames``
.. _geopandas.GeoDataFrames: https://geopandas.readthedocs.io/en/latest/docs/user_guide/data_structures.html#geodataframe
.. |pandas.DataFrames| replace:: ``pandas.DataFrames``
.. _pandas.DataFrames: https://pandas.pydata.org/docs/user_guide/dsintro.html#dataframe

What’s here?
------------

We’ve taken a grab-and-go approach to installation and usage of
Hydrotools. This means, in line with a standard toolbox, you will
typically install just the tool or tools that get your job done without
having to install all the other tools available. This means a lighter
installation load and that tools can be added to the toolbox, without
affecting your workflows!

It should be noted, we commonly refer to individual tools in HydroTools as a
subpackage or by their name (e.g. ``nwis_client``). You will find this lingo in both
issues and documentation.

Currently the repository has the following subpackages:

-  nwis_client: Provides easy to use methods for retrieving data from
   the `USGS NWIS Instantaneous Values (IV) Web
   Service <https://waterservices.usgs.gov/rest/IV-Service.html>`__.
-  \_restclient: A generic REST client with built in cache that make the
   construction and retrieval of GET requests painless.
-  metrics: Variety of methods used to compute common evaluation metrics.

Installation
------------

In accordance with the python community, we support and advise the usage
of virtual environments in any workflow using python. In the following
installation guide, we use python’s built-in ``venv`` module to create a
virtual environment in which the tools will be installed. Note this is
just personal preference, any python virtual environment manager should
work just fine (``conda``, ``pipenv``, etc. ).

.. code:: bash

   # Create and activate python environment, requires python >= 3.8
   $ python3 -m venv venv
   $ source venv/bin/activate
   $ python3 -m pip install --upgrade pip

   # Install nwis_client
   $ python3 -m pip install git+https://github.com/NOAA-OWP/hydrotools.git#subdirectory=python/nwis_client

   # Install _restclient
   $ python3 -m pip install git+https://github.com/NOAA-OWP/hydrotools.git#subdirectory=python/_restclient

   # Install metrics
   $ python3 -m pip install git+https://github.com/NOAA-OWP/hydrotools.git#subdirectory=python/metrics

UTC Time
--------

Note: the canonical ``pandas.DataFrames`` used by HydroTools use
time-zone naive datetimes that assume UTC time. In general, do not
assume methods are compatible with time-zone aware datetimes or
timestamps. Expect methods to transform time-zone aware datetimes and
timestamps into their timezone naive counterparts at UTC time.
