"""Views for Vserver Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import vserver as forms


class VserverView(generic.ObjectView):
    """Detail view."""

    queryset = models.Vserver.objects.all()


class VserverListView(generic.ObjectListView):
    """List view."""

    queryset = models.Vserver.objects.all()
    filterset = filters.VserverFilterSet
    filterset_form = forms.VserverFilterForm
    table = tables.VserverTable
    action_buttons = ("import", "export", "add")


class VserverCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.Vserver
    queryset = models.Vserver.objects.all()
    model_form = forms.VserverForm


class VserverDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.Vserver
    queryset = models.Vserver.objects.all()


class VserverEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.Vserver
    queryset = models.Vserver.objects.all()
    model_form = forms.VserverForm


class VserverBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Vserver records."""

    queryset = models.Vserver.objects.all()
    table = tables.VserverTable


class VserverBulkImportView(generic.BulkImportView):
    """View for importing one or more Vserver records."""

    queryset = models.Vserver.objects.all()
    model_form = forms.VserverCSVForm
    table = tables.VserverTable


class VserverBulkEditView(generic.BulkEditView):
    """View for editing one or more Vserver records."""

    queryset = models.Vserver.objects.all()
    table = tables.VserverTable
    form = forms.VserverForm
