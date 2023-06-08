"""Views for ServiceGroupMemberBinding Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import servicegroupmemberbinding as forms


class ServiceGroupMemberBindingView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServiceGroupMemberBinding.objects.all()


class ServiceGroupMemberBindingListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServiceGroupMemberBinding.objects.all()
    filterset = filters.ServiceGroupMemberBindingFilterSet
    filterset_form = forms.ServiceGroupMemberBindingFilterForm
    table = tables.ServiceGroupMemberBindingTable
    action_buttons = ("import", "export", "add")


class ServiceGroupMemberBindingCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.ServiceGroupMemberBinding
    queryset = models.ServiceGroupMemberBinding.objects.all()
    model_form = forms.ServiceGroupMemberBindingForm


class ServiceGroupMemberBindingDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.ServiceGroupMemberBinding
    queryset = models.ServiceGroupMemberBinding.objects.all()


class ServiceGroupMemberBindingEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.ServiceGroupMemberBinding
    queryset = models.ServiceGroupMemberBinding.objects.all()
    model_form = forms.ServiceGroupMemberBindingBulkEditForm


class ServiceGroupMemberBindingBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServiceGroupMemberBinding records."""

    queryset = models.ServiceGroupMemberBinding.objects.all()
    table = tables.ServiceGroupMemberBindingTable


class ServiceGroupMemberBindingBulkImportView(generic.BulkImportView):
    """View for importing one or more ServiceGroupMemberBinding records."""

    queryset = models.ServiceGroupMemberBinding.objects.all()
    model_form = forms.ServiceGroupMemberBindingCSVForm
    table = tables.ServiceGroupMemberBindingTable


class ServiceGroupMemberBindingBulkEditView(generic.BulkEditView):
    """View for editing one or more ServiceGroupMemberBinding records."""

    queryset = models.ServiceGroupMemberBinding.objects.all()
    table = tables.ServiceGroupMemberBindingTable
    form = forms.ServiceGroupMemberBindingBulkEditForm
