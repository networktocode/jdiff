"""Views for Monitor Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import monitor as forms


class MonitorView(generic.ObjectView):
    """Detail view."""

    queryset = models.Monitor.objects.all()


class MonitorListView(generic.ObjectListView):
    """List view."""

    queryset = models.Monitor.objects.all()
    filterset = filters.MonitorFilterSet
    filterset_form = forms.MonitorFilterForm
    table = tables.MonitorTable
    action_buttons = ("import", "export", "add")


class MonitorCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.Monitor
    queryset = models.Monitor.objects.all()
    model_form = forms.MonitorForm


class MonitorDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.Monitor
    queryset = models.Monitor.objects.all()


class MonitorEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.Monitor
    queryset = models.Monitor.objects.all()
    model_form = forms.MonitorBulkEditForm


class MonitorBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Monitor records."""

    queryset = models.Monitor.objects.all()
    table = tables.MonitorTable


class MonitorBulkImportView(generic.BulkImportView):
    """View for importing one or more Monitor records."""

    queryset = models.Monitor.objects.all()
    model_form = forms.MonitorCSVForm
    table = tables.MonitorTable


class MonitorBulkEditView(generic.BulkEditView):
    """View for editing one or more Monitor records."""

    queryset = models.Monitor.objects.all()
    table = tables.MonitorTable
    form = forms.MonitorBulkEditForm
