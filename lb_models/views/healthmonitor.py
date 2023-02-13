"""Views for VIPHealthMonitor Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import healthmonitor as forms


class VIPHealthMonitorView(generic.ObjectView):
    """Detail view."""

    queryset = models.VIPHealthMonitor.objects.all()


class VIPHealthMonitorListView(generic.ObjectListView):
    """List view."""

    queryset = models.VIPHealthMonitor.objects.all()
    filterset = filters.VIPHealthMonitorFilterSet
    filterset_form = forms.VIPHealthMonitorFilterForm
    table = tables.VIPHealthMonitorTable
    action_buttons = ("import", "export", "add")


class VIPHealthMonitorCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.VIPHealthMonitor
    queryset = models.VIPHealthMonitor.objects.all()
    model_form = forms.VIPHealthMonitorForm


class VIPHealthMonitorDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.VIPHealthMonitor
    queryset = models.VIPHealthMonitor.objects.all()


class VIPHealthMonitorEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.VIPHealthMonitor
    queryset = models.VIPHealthMonitor.objects.all()
    model_form = forms.VIPHealthMonitorForm


class VIPHealthMonitorBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more VIPHealthMonitor records."""

    queryset = models.VIPHealthMonitor.objects.all()
    table = tables.VIPHealthMonitorTable


class VIPHealthMonitorBulkImportView(generic.BulkImportView):
    """View for importing one or more VIPHealthMonitor records."""

    queryset = models.VIPHealthMonitor.objects.all()
    model_form = forms.VIPHealthMonitorCSVForm
    table = tables.VIPHealthMonitorTable


class VIPHealthMonitorBulkEditView(generic.BulkEditView):
    """View for editing one or more VIPHealthMonitor records."""

    queryset = models.VIPHealthMonitor.objects.all()
    table = tables.VIPHealthMonitorTable
    form = forms.VIPHealthMonitorForm
