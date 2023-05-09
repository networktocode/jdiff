"""Menu items."""

from nautobot.extras.plugins import PluginMenuButton, PluginMenuItem
from nautobot.utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:lb_models:customerappprofile_list",
        link_text="Customer App Profile",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:customerappprofile_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:customerappprofile_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:monitor_list",
        link_text="Monitor",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:monitor_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:monitor_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:server_list",
        link_text="Server",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:server_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:server_import",
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
        link="plugins:lb_models:servicegroupmemberbinding_list",
        link_text="Service Group Member Binding",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:servicegroupmemberbinding_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:servicegroupmemberbinding_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:servicegroupmonitorbinding_list",
        link_text="Service Group Monitor Binding",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:servicegroupmonitorbinding_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:servicegroupmonitorbinding_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:serverservicegroupbinding_list",
        link_text="Server Service Group Binding",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:serverservicegroupbinding_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:serverservicegroupbinding_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:sslcertkey_list",
        link_text="SSL Cert Key",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:sslcertkey_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:sslcertkey_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:sslserverbinding_list",
        link_text="SSL Server Binding",
        buttons=(
            PluginMenuButton(
                link="plugins:lb_models:sslserverbinding_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:lb_models:sslserverbinding_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:lb_models:vserver_list",
        link_text="Vserver",
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
