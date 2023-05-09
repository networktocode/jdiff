"""Views for Server Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import server as forms


class ServerView(generic.ObjectView):
    """Detail view."""

    queryset = models.Server.objects.all()


class ServerListView(generic.ObjectListView):
    """List view."""

    queryset = models.Server.objects.all()
    filterset = filters.ServerFilterSet
    filterset_form = forms.ServerFilterForm
    table = tables.ServerTable
    action_buttons = ("import", "export", "add")


class ServerCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.Server
    queryset = models.Server.objects.all()
    model_form = forms.ServerForm


class ServerDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.Server
    queryset = models.Server.objects.all()


class ServerEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.Server
    queryset = models.Server.objects.all()
    model_form = forms.ServerForm


class ServerBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Server records."""

    queryset = models.Server.objects.all()
    table = tables.ServerTable


class ServerBulkImportView(generic.BulkImportView):
    """View for importing one or more Server records."""

    queryset = models.Server.objects.all()
    model_form = forms.ServerCSVForm
    table = tables.ServerTable


class ServerBulkEditView(generic.BulkEditView):
    """View for editing one or more Server records."""

    queryset = models.Server.objects.all()
    table = tables.ServerTable
    form = forms.ServerForm
