#!/usr/bin/env python3
import pytest


def pytest_addoption(parser):
    # Add flag to `pytest` to run tests decorated with:
    # @pytest.mark.slow
    # Mark was defined in pytest.ini
    parser.addoption(
        "-S",
        "--run-slow",
        action="store_true",
        default=False,
        dest="runslow",
        help="run slow tests",
    )


def pytest_configure(config):
    if config.option.runslow is False:
        # If --run-slow not specified, do not run slow marked tests by default
        setattr(config.option, "markexpr", "not slow")
