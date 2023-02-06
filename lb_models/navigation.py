"""Menu items."""

from nautobot.extras.plugins import PluginMenuButton, PluginMenuItem
from nautobot.utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:lb_models:vipcertficate_list",
        link_text="VIP Certificates",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:vipcertficate_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:vipcertficate_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
)
