from .gcp import NWMDataService
import warnings

warning_message = "Importing gcp_client is deprecated. Import hydrotools.nwm_client.gcp"
warnings.warn(warning_message, UserWarning)
