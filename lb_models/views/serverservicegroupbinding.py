"""Views for ServerServiceGroupBinding Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import servicegroupmemberbinding as forms


class ServerServiceGroupBindingView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServerServiceGroupBinding.objects.all()


class ServerServiceGroupBindingListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServerServiceGroupBinding.objects.all()
    filterset = filters.ServerServiceGroupBindingFilterSet
    filterset_form = forms.ServerServiceGroupBindingFilterForm
    table = tables.ServerServiceGroupBindingTable
    action_buttons = ("import", "export", "add")


class ServerServiceGroupBindingCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.ServerServiceGroupBinding
    queryset = models.ServerServiceGroupBinding.objects.all()
    model_form = forms.ServerServiceGroupBindingForm


class ServerServiceGroupBindingDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.ServerServiceGroupBinding
    queryset = models.ServerServiceGroupBinding.objects.all()


class ServerServiceGroupBindingEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.ServerServiceGroupBinding
    queryset = models.ServerServiceGroupBinding.objects.all()
    model_form = forms.ServerServiceGroupBindingForm


class ServerServiceGroupBindingBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServerServiceGroupBinding records."""

    queryset = models.ServerServiceGroupBinding.objects.all()
    table = tables.ServerServiceGroupBindingTable


class ServerServiceGroupBindingBulkImportView(generic.BulkImportView):
    """View for importing one or more ServerServiceGroupBinding records."""

    queryset = models.ServerServiceGroupBinding.objects.all()
    model_form = forms.ServerServiceGroupBindingCSVForm
    table = tables.ServerServiceGroupBindingTable


class ServerServiceGroupBindingBulkEditView(generic.BulkEditView):
    """View for editing one or more ServerServiceGroupBinding records."""

    queryset = models.ServerServiceGroupBinding.objects.all()
    table = tables.ServerServiceGroupBindingTable
    form = forms.ServerServiceGroupBindingForm
