"""Menu items."""

from nautobot.extras.plugins import PluginMenuButton, PluginMenuItem
from nautobot.utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:lb_models:vipcertificate_list",
        link_text="VIP Certificates",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:vipcertificate_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:vipcertificate_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:vippoolmember_list",
        link_text="VIP Poll Member",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:vippoolmember_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:vippoolmember_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:viphealthmonitor_list",
        link_text="VIP Health Monitor",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:viphealthmonitor_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:viphealthmonitor_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:vippool_list",
        link_text="VIP Pool",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:vippool_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:vippool_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:vip_list",
        link_text="VIP",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:vip_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:vip_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
)
