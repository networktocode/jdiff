"""Menu items."""

from nautobot.extras.plugins import PluginMenuButton, PluginMenuItem
from nautobot.utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:lb_models:certificate_list",
        link_text="Certificate",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:certificate_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:certificate_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:servicegroupbinding_list",
        link_text="Service Group Binding",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:servicegroupbinding_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:servicegroupbinding_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:healthmonitor_list",
        link_text="Health Monitor",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:healthmonitor_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:healthmonitor_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:servicegroup_list",
        link_text="Service Group",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:servicegroup_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:servicegroup_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:vserver_list",
        link_text="vserver",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:vserver_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:vserver_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
)
