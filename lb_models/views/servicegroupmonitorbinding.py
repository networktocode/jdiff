"""Views for ServiceGroupMonitorBinding Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import servicegroupmonitorbinding as forms


class ServiceGroupMonitorBindingView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServiceGroupMonitorBinding.objects.all()


class ServiceGroupMonitorBindingListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServiceGroupMonitorBinding.objects.all()
    filterset = filters.ServiceGroupMonitorBindingFilterSet
    filterset_form = forms.ServiceGroupMonitorBindingFilterForm
    table = tables.ServiceGroupMonitorBindingTable
    action_buttons = ("import", "export", "add")


class ServiceGroupMonitorBindingCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.ServiceGroupMonitorBinding
    queryset = models.ServiceGroupMonitorBinding.objects.all()
    model_form = forms.ServiceGroupMonitorBindingForm


class ServiceGroupMonitorBindingDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.ServiceGroupMonitorBinding
    queryset = models.ServiceGroupMonitorBinding.objects.all()


class ServiceGroupMonitorBindingEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.ServiceGroupMonitorBinding
    queryset = models.ServiceGroupMonitorBinding.objects.all()
    model_form = forms.ServiceGroupMonitorBindingForm


class ServiceGroupMonitorBindingBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServiceGroupMonitorBinding records."""

    queryset = models.ServiceGroupMonitorBinding.objects.all()
    table = tables.ServiceGroupMonitorBindingTable


class ServiceGroupMonitorBindingBulkImportView(generic.BulkImportView):
    """View for importing one or more ServiceGroupMonitorBinding records."""

    queryset = models.ServiceGroupMonitorBinding.objects.all()
    model_form = forms.ServiceGroupMonitorBindingCSVForm
    table = tables.ServiceGroupMonitorBindingTable


class ServiceGroupMonitorBindingBulkEditView(generic.BulkEditView):
    """View for editing one or more ServiceGroupMonitorBinding records."""

    queryset = models.ServiceGroupMonitorBinding.objects.all()
    table = tables.ServiceGroupMonitorBindingTable
    form = forms.ServiceGroupMonitorBindingForm
