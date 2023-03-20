"""Views for vserver Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import vserver as forms


class vserverView(generic.ObjectView):
    """Detail view."""

    queryset = models.vserver.objects.all()


class vserverListView(generic.ObjectListView):
    """List view."""

    queryset = models.vserver.objects.all()
    filterset = filters.vserverFilterSet
    filterset_form = forms.vserverFilterForm
    table = tables.vserverTable
    action_buttons = ("import", "export", "add")


class vserverCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.vserver
    queryset = models.vserver.objects.all()
    model_form = forms.vserverForm


class vserverDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.vserver
    queryset = models.vserver.objects.all()


class vserverEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.vserver
    queryset = models.vserver.objects.all()
    model_form = forms.vserverForm


class vserverBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more vserver records."""

    queryset = models.vserver.objects.all()
    table = tables.vserverTable


class vserverBulkImportView(generic.BulkImportView):
    """View for importing one or more vserver records."""

    queryset = models.vserver.objects.all()
    model_form = forms.vserverCSVForm
    table = tables.vserverTable


class vserverBulkEditView(generic.BulkEditView):
    """View for editing one or more vserver records."""

    queryset = models.vserver.objects.all()
    table = tables.vserverTable
    form = forms.vserverForm
