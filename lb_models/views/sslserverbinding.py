"""Views for SSLServerBinding Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import sslserverbinding as forms


class SSLServerBindingView(generic.ObjectView):
    """Detail view."""

    queryset = models.SSLServerBinding.objects.all()


class SSLServerBindingListView(generic.ObjectListView):
    """List view."""

    queryset = models.SSLServerBinding.objects.all()
    filterset = filters.SSLServerBindingFilterSet
    filterset_form = forms.SSLServerBindingFilterForm
    table = tables.SSLServerBindingTable
    action_buttons = ("import", "export", "add")


class SSLServerBindingCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.SSLServerBinding
    queryset = models.SSLServerBinding.objects.all()
    model_form = forms.SSLServerBindingForm


class SSLServerBindingDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.SSLServerBinding
    queryset = models.SSLServerBinding.objects.all()


class SSLServerBindingEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.SSLServerBinding
    queryset = models.SSLServerBinding.objects.all()
    model_form = forms.SSLServerBindingForm


class SSLServerBindingBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more SSLServerBinding records."""

    queryset = models.SSLServerBinding.objects.all()
    table = tables.SSLServerBindingTable


class SSLServerBindingBulkImportView(generic.BulkImportView):
    """View for importing one or more SSLServerBinding records."""

    queryset = models.SSLServerBinding.objects.all()
    model_form = forms.SSLServerBindingCSVForm
    table = tables.SSLServerBindingTable


class SSLServerBindingBulkEditView(generic.BulkEditView):
    """View for editing one or more SSLServerBinding records."""

    queryset = models.SSLServerBinding.objects.all()
    table = tables.SSLServerBindingTable
    form = forms.SSLServerBindingForm
