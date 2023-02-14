"""Views for VIP Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import vip as forms


class VIPView(generic.ObjectView):
    """Detail view."""

    queryset = models.VIP.objects.all()


class VIPListView(generic.ObjectListView):
    """List view."""

    queryset = models.VIP.objects.all()
    filterset = filters.VIPFilterSet
    filterset_form = forms.VIPFilterForm
    table = tables.VIPTable
    action_buttons = ("import", "export", "add")


class VIPCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.VIP
    queryset = models.VIP.objects.all()
    model_form = forms.VIPForm


class VIPDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.VIP
    queryset = models.VIP.objects.all()


class VIPEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.VIP
    queryset = models.VIP.objects.all()
    model_form = forms.VIPForm


class VIPBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more VIP records."""

    queryset = models.VIP.objects.all()
    table = tables.VIPTable


class VIPBulkImportView(generic.BulkImportView):
    """View for importing one or more VIP records."""

    queryset = models.VIP.objects.all()
    model_form = forms.VIPCSVForm
    table = tables.VIPTable


class VIPBulkEditView(generic.BulkEditView):
    """View for editing one or more VIP records."""

    queryset = models.VIP.objects.all()
    table = tables.VIPTable
    form = forms.VIPForm
