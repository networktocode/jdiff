"""Views for Customer Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import customer as forms


class CustomerView(generic.ObjectView):
    """Detail view."""

    queryset = models.Customer.objects.all()


class CustomerListView(generic.ObjectListView):
    """List view."""

    queryset = models.Customer.objects.all()
    filterset = filters.CustomerFilterSet
    filterset_form = forms.CustomerFilterForm
    table = tables.CustomerTable
    action_buttons = ("import", "export", "add")


class CustomerCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.Customer
    queryset = models.Customer.objects.all()
    model_form = forms.CustomerForm


class CustomerDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.Customer
    queryset = models.Customer.objects.all()


class CustomerEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.Customer
    queryset = models.Customer.objects.all()
    model_form = forms.CustomerForm


class CustomerBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Customer records."""

    queryset = models.Customer.objects.all()
    table = tables.CustomerTable


class CustomerBulkImportView(generic.BulkImportView):
    """View for importing one or more Customer records."""

    queryset = models.Customer.objects.all()
    model_form = forms.CustomerCSVForm
    table = tables.CustomerTable


class CustomerBulkEditView(generic.BulkEditView):
    """View for editing one or more Customer records."""

    queryset = models.Customer.objects.all()
    table = tables.CustomerTable
    form = forms.CustomerForm
