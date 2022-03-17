import pytest
from hydrotools.nwis_client import cli
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

def test_cli():
    """Normaly would use click.testing.CLiRunner. However, this does not appear to be async friendly."""
    with TemporaryDirectory() as tdir:
        # Test default parameters
        result1 = subprocess.run([
            "nwis-client", "01013500", "02146470", "-o", f"{tdir}/test_output_1.csv"
        ])
        assert result1.returncode == 0
        assert Path(f"{tdir}/test_output_1.csv").exists()

        # Test other parameters
        result2 = subprocess.run([
            "nwis-client",
            '-s', '2022-01-01',
            '-e', '2022-01-02',
            '-p', '00065',
            '01013500', '02146470', "-o", f"{tdir}/test_output_2.csv"])
        assert result2.returncode == 0
        assert Path(f"{tdir}/test_output_2.csv").exists()

def test_comments_header():
    """Normaly would use click.testing.CLiRunner. However, this does not appear to be async friendly."""
    with TemporaryDirectory() as tdir:
        # Output file
        ofile = Path(tdir) / "test_output.csv"

        # Disable comments and header
        result2 = subprocess.run([
            "nwis-client",
            '--no-comments', '--no-header',
            '01013500', '02146470', "-o", str(ofile)])
        assert result2.returncode == 0
        assert ofile.exists()

        # File should only have two lines
        with ofile.open('r') as fi:
            count = len([l for l in fi])
            assert count == 2
            