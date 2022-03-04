import pytest
from click.testing import CliRunner
from hydrotools.nwis_client.cli import run
from pathlib import Path

def test_cli():
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Test default parameters
        result1 = runner.invoke(run, ['01013500', '02146470', "test_output_1.csv"])
        assert result1.exit_code == 0
        assert Path("test_output_1.csv").exists()

        # Test other parameters
        result2 = runner.invoke(run, [
            '-s', '2022-01-01',
            '-e', '2022-01-02',
            '-p', '00065',
            '01013500', '02146470', "test_output_2.csv"])
        assert result2.exit_code == 0
        assert Path("test_output_2.csv").exists()
