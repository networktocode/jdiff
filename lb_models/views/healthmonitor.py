"""Views for HealthMonitor Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import healthmonitor as forms


class HealthMonitorView(generic.ObjectView):
    """Detail view."""

    queryset = models.HealthMonitor.objects.all()


class HealthMonitorListView(generic.ObjectListView):
    """List view."""

    queryset = models.HealthMonitor.objects.all()
    filterset = filters.HealthMonitorFilterSet
    filterset_form = forms.HealthMonitorFilterForm
    table = tables.HealthMonitorTable
    action_buttons = ("import", "export", "add")


class HealthMonitorCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.HealthMonitor
    queryset = models.HealthMonitor.objects.all()
    model_form = forms.HealthMonitorForm


class HealthMonitorDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.HealthMonitor
    queryset = models.HealthMonitor.objects.all()


class HealthMonitorEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.HealthMonitor
    queryset = models.HealthMonitor.objects.all()
    model_form = forms.HealthMonitorForm


class HealthMonitorBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more HealthMonitor records."""

    queryset = models.HealthMonitor.objects.all()
    table = tables.HealthMonitorTable


class HealthMonitorBulkImportView(generic.BulkImportView):
    """View for importing one or more HealthMonitor records."""

    queryset = models.HealthMonitor.objects.all()
    model_form = forms.HealthMonitorCSVForm
    table = tables.HealthMonitorTable


class HealthMonitorBulkEditView(generic.BulkEditView):
    """View for editing one or more HealthMonitor records."""

    queryset = models.HealthMonitor.objects.all()
    table = tables.HealthMonitorTable
    form = forms.HealthMonitorForm
