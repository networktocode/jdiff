"""Plugin declaration for cu_allspice_lb_management."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig


class CuAllspiceLbManagementConfig(PluginConfig):
    """Plugin configuration for the cu_allspice_lb_management plugin."""

    name = "cu_allspice_lb_management"
    verbose_name = "cu-allspice-lb-management"
    version = __version__
    author = "Network to Code, LLC"
    description = "cu-allspice-lb-management."
    base_url = "cu-allspice-lb-management"
    required_settings = []
    min_version = "1.4"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = CuAllspiceLbManagementConfig  # pylint:disable=invalid-name
