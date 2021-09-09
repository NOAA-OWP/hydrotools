"""
===============
File Downloader
===============
Tool for downloading files.

Classes
-------
FileDownloader
"""
import asyncio
import aiohttp
import aiofiles
from urllib.parse import unquote
from pathlib import Path
from typing import Iterable, Union
import warnings

class FileDownloader:

    def __init__(self, output_directory: Union[str, Path] = Path("."), 
        create_directory: bool = False) -> None:
        """Initialize File Downloader object with specified output directory.
        
        Parameters
        ----------
        output_directory: str, pathlib.Path, optional, default "."
            Output directory where files are written.
        create_directory: bool, options, default False
            Indicates whether to create the output directory if it does not 
            exist.
            
        Returns
        -------
        None
        """
        # Set output directory
        self._output_directory = Path(output_directory).expanduser().resolve()

        # Set directory creation
        self._create_directory = bool(create_directory)

    async def get_file(self, url: str, session: aiohttp.ClientSession) -> None:
        """Download a single file.
        
        Parameters
        ----------
        url: str, required
            URL path to file.
        session: aiohttp.ClientSession, required
            Session object used for retrieval.
            
        Returns
        -------
        None
        """
        # Retrieve a single file
        async with session.get(url) as response:
            # Extract file name
            filename = unquote(url).split("/")[-1]

            # Warn if unable to locate file
            if response.status >= 400:
                warnings.warn(f"Unable to download {filename}", RuntimeWarning)
                return

            # Construct output file path
            output_file = self.output_directory / filename

            # Stream download
            async with aiofiles.open(output_file, 'wb') as fo:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    await fo.write(chunk)

    async def get_files(self, urls: Iterable[str]) -> None:
        """Asynchronously download multiple files.
        
        Parameters
        ----------
        urls: iterable of str, required
            Iterable of url strings.
            
        Returns
        -------
        None
        """
        # Retrieve each file
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.get_file(url, session) for url in urls])

    def get(self, urls: Iterable[str]) -> None:
        """Setup event loop and asynchronously download multiple files. If 
        FileDownloader.create_directory is True, an output directory will be 
        created.
        
        Parameters
        ----------
        urls: iterable of str, required
            Iterable of url strings.
            
        Returns
        -------
        None
        """
        # Check output directory, optionally create
        if not self.output_directory.exists():
            if self.create_directory:
                self.output_directory.mkdir(parents=True)
            else:
                message = f"{self.output_directory} does not exist."
                raise FileNotFoundError(message)

        # Start event loop to retrieve files
        asyncio.run(self.get_files(urls))

    @property
    def output_directory(self):
        return self._output_directory

    @output_directory.setter
    def output_directory(self, output_directory: Union[str, Path]):
        self._output_directory = Path(output_directory).expanduser().resolve()

    @property
    def create_directory(self):
        return self._create_directory

    @create_directory.setter
    def create_directory(self, create_directory: bool):
        self._create_directory = bool(create_directory)