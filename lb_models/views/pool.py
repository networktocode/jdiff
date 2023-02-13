"""Views for VIPPool Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import pool as forms


class VIPPoolView(generic.ObjectView):
    """Detail view."""

    queryset = models.VIPPool.objects.all()


class VIPPoolListView(generic.ObjectListView):
    """List view."""

    queryset = models.VIPPool.objects.all()
    filterset = filters.VIPPoolFilterSet
    filterset_form = forms.VIPPoolFilterForm
    table = tables.VIPPoolTable
    action_buttons = ("import", "export", "add")


class VIPPoolCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.VIPPool
    queryset = models.VIPPool.objects.all()
    model_form = forms.VIPPoolForm


class VIPPoolDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.VIPPool
    queryset = models.VIPPool.objects.all()


class VIPPoolEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.VIPPool
    queryset = models.VIPPool.objects.all()
    model_form = forms.VIPPoolForm


class VIPPoolBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more VIPPool records."""

    queryset = models.VIPPool.objects.all()
    table = tables.VIPPoolTable


class VIPPoolBulkImportView(generic.BulkImportView):
    """View for importing one or more VIPPool records."""

    queryset = models.VIPPool.objects.all()
    model_form = forms.VIPPoolCSVForm
    table = tables.VIPPoolTable


class VIPPoolBulkEditView(generic.BulkEditView):
    """View for editing one or more VIPPool records."""

    queryset = models.VIPPool.objects.all()
    table = tables.VIPPoolTable
    form = forms.VIPPoolForm
