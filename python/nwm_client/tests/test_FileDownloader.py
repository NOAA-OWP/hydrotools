import pytest
from hydrotools.nwm_client_new.FileDownloader import FileDownloader
from tempfile import TemporaryDirectory

def test_parameters():
    with TemporaryDirectory() as td:
        downloader = FileDownloader(output_directory=td)
        assert downloader.output_directory
        assert not downloader.create_directory
        assert downloader.ssl_context
        assert downloader.limit == 10

@pytest.mark.slow
def test_get():
    with TemporaryDirectory() as td:
        downloader = FileDownloader(output_directory=td)
        downloader.get(
            [("https://pandas.pydata.org/docs/user_guide/index.html","index.html")]
            )
        ofile = downloader.output_directory / "index.html"
        assert ofile.exists()

@pytest.mark.slow
def test_overwrite_warning():
    with TemporaryDirectory() as td:
        with pytest.warns(UserWarning):
            downloader = FileDownloader(output_directory=td)
            downloader.get(
                [("https://pandas.pydata.org/docs/user_guide/index.html","index.html")]
                )
            ofile = downloader.output_directory / "index.html"
            downloader.get(
                [("https://pandas.pydata.org/docs/user_guide/index.html","index.html")]
                )
