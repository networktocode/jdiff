"""Plugin declaration for lb_models."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig


class CuAllspiceLbManagementConfig(PluginConfig):
    """Plugin configuration for the lb_models plugin."""

    name = "lb_models"
    verbose_name = "lb_models"
    version = __version__
    author = "Network to Code, LLC"
    description = "lb_models."
    base_url = "lb_models"
    required_settings = []
    min_version = "1.4"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = CuAllspiceLbManagementConfig  # pylint:disable=invalid-name
