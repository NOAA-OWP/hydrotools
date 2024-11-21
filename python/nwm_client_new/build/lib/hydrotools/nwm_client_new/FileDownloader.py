"""
===============
File Downloader
===============
Tool for downloading files asynchronously.

Classes
-------
FileDownloader
"""
import asyncio
import ssl
import aiohttp
import aiofiles
from pathlib import Path
from typing import List, Tuple, Union
import warnings
from http import HTTPStatus

class FileDownloader:
    """Provides a convenient interface to download a list of files
    asynchronously using HTTP.
    """

    def __init__(
        self,
        output_directory: Union[str, Path] = Path("."), 
        create_directory: bool = False,
        ssl_context: ssl.SSLContext = ssl.create_default_context(),
        limit: int = 10
        ) -> None:
        """Initialize File Downloader object with specified output directory.
        
        Parameters
        ----------
        output_directory: str, pathlib.Path, optional, default "."
            Output directory where files are written.
        create_directory: bool, options, default False
            Indicates whether to create the output directory if it does not 
            exist.
        ssl_context : ssl.SSLContext, optional, default context
            SSL configuration context.
        limit: int, optional, default 10
            Number of simultaneous connections.
            
        Returns
        -------
        None
        """
        # Set output directory
        self.output_directory = output_directory

        # Set directory creation
        self.create_directory = create_directory

        # Setup SSL context
        self.ssl_context = ssl_context

        # Set limit
        self.limit = limit

    async def get_file(
        self,
        url: str,
        filename: str,
        session: aiohttp.ClientSession
        ) -> None:
        """Download a single file.
        
        Parameters
        ----------
        url: str, required
            URL path to file.
        filename: str, required
            Local filename used to write downloaded file. This will save the file 
            to self.output_directory/filename
        session: aiohttp.ClientSession, required
            Session object used for retrieval.
            
        Returns
        -------
        None
        """
        # Retrieve a single file
        async with session.get(url, ssl=self.ssl_context, timeout=900) as response:
            # Warn if unable to locate file
            if response.status != HTTPStatus.OK:
                status = HTTPStatus(response.status_code)
                message = (
                    f"HTTP Status: {status.value}" + 
                    f" - {status.phrase}" + 
                    f" - {status.description}\n" + 
                    f"{response.url}"
                    )
                warnings.warn(message, RuntimeWarning)
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

    async def get_files(self, src_dst_list: List[Tuple[str,str]]) -> None:
        """Asynchronously download multiple files.
        
        Parameters
        ----------
        src_dst_list: List[Tuple[str,str]], required
            List of tuples containing two strings. The first string is the 
            source URL from which to retrieve a file, the second string is the
            local filename where the file will be saved.
            
        Returns
        -------
        None
        """
        # Retrieve each file
        connector = aiohttp.TCPConnector(limit=self.limit)
        async with aiohttp.ClientSession(connector=connector) as session:
            await asyncio.gather(*[self.get_file(url, filename, session) for url, filename in src_dst_list])

    def get(self, src_dst_list: List[Tuple[str,str]], overwrite: bool = False) -> None:
        """Setup event loop and asynchronously download multiple files. If 
        self.create_directory is True, an output directory will be 
        created if needed.
        
        Parameters
        ----------
        src_dst_list: List[Tuple[str,str]], required
            List of tuples containing two strings. The first string is the 
            source URL from which to retrieve a file, the second string is the
            local filename where the file will be saved.
        overwrite: bool, optional, default False
            If True will overwrite destination file, if it exists. If False, 
            download of this file is skipped.
            
        Returns
        -------
        None

        Examples
        --------
        >>> from nwm_client_new.FileDownloader import FileDownloader
        >>> downloader = FileDownloader(output_directory="my_output")

        >>> # This will download the pandas homepage and save it to "my_output/index.html"
        >>> downloader.get(
        >>>     [("https://pandas.pydata.org/docs/user_guide/index.html","index.html")]
        >>>     )
        """
        # Shorten list to files that do not exist
        if not overwrite:
            short = []
            for src, dst in src_dst_list:
                if (self.output_directory / dst).exists():
                    message = f"File exists, skipping download of {self.output_directory / dst}"
                    warnings.warn(message, UserWarning)
                    continue
                short.append((src, dst))
            src_dst_list = short
        
        # Check output directory, optionally create
        if not self.output_directory.exists():
            if self.create_directory:
                self.output_directory.mkdir(parents=True)
            else:
                message = f"{self.output_directory} does not exist."
                raise FileNotFoundError(message)

        # Start event loop to retrieve files
        asyncio.run(self.get_files(src_dst_list))

    @property
    def output_directory(self) -> Path:
        return self._output_directory

    @output_directory.setter
    def output_directory(self, output_directory: Union[str, Path]):
        self._output_directory = Path(output_directory).expanduser().resolve()

    @property
    def create_directory(self) -> bool:
        return self._create_directory

    @create_directory.setter
    def create_directory(self, create_directory: bool):
        self._create_directory = bool(create_directory)

    @property
    def ssl_context(self) -> ssl.SSLContext:
        return self._ssl_context

    @ssl_context.setter
    def ssl_context(self, ssl_context: ssl.SSLContext) -> None:
        self._ssl_context = ssl_context

    @property
    def limit(self) -> int:
        return self._limit

    @limit.setter
    def limit(self, limit: int) -> None:
        self._limit = limit
