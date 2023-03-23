"""Views for ServiceGroupBinding Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import servicegroupbinding as forms


class ServiceGroupBindingView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServiceGroupBinding.objects.all()


class ServiceGroupBindingListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServiceGroupBinding.objects.all()
    filterset = filters.ServiceGroupBindingFilterSet
    filterset_form = forms.ServiceGroupBindingFilterForm
    table = tables.ServiceGroupBindingTable
    action_buttons = ("import", "export", "add")


class ServiceGroupBindingCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.ServiceGroupBinding
    queryset = models.ServiceGroupBinding.objects.all()
    model_form = forms.ServiceGroupBindingForm


class ServiceGroupBindingDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.ServiceGroupBinding
    queryset = models.ServiceGroupBinding.objects.all()


class ServiceGroupBindingEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.ServiceGroupBinding
    queryset = models.ServiceGroupBinding.objects.all()
    model_form = forms.ServiceGroupBindingForm


class ServiceGroupBindingBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServiceGroupBinding records."""

    queryset = models.ServiceGroupBinding.objects.all()
    table = tables.ServiceGroupBindingTable


class ServiceGroupBindingBulkImportView(generic.BulkImportView):
    """View for importing one or more ServiceGroupBinding records."""

    queryset = models.ServiceGroupBinding.objects.all()
    model_form = forms.ServiceGroupBindingCSVForm
    table = tables.ServiceGroupBindingTable


class ServiceGroupBindingBulkEditView(generic.BulkEditView):
    """View for editing one or more ServiceGroupBinding records."""

    queryset = models.ServiceGroupBinding.objects.all()
    table = tables.ServiceGroupBindingTable
    form = forms.ServiceGroupBindingForm
