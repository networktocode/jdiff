"""Views for SSLCertKey Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import sslcertkey as forms


class SSLCertKeyView(generic.ObjectView):
    """Detail view."""

    queryset = models.SSLCertKey.objects.all()


class SSLCertKeyListView(generic.ObjectListView):
    """List view."""

    queryset = models.SSLCertKey.objects.all()
    filterset = filters.SSLCertKeyFilterSet
    filterset_form = forms.SSLCertKeyFilterForm
    table = tables.SSLCertKeyTable
    action_buttons = ("import", "export", "add")


class SSLCertKeyCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.SSLCertKey
    queryset = models.SSLCertKey.objects.all()
    model_form = forms.SSLCertKeyForm


class SSLCertKeyDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.SSLCertKey
    queryset = models.SSLCertKey.objects.all()


class SSLCertKeyEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.SSLCertKey
    queryset = models.SSLCertKey.objects.all()
    model_form = forms.SSLCertKeyBulkEditForm


class SSLCertKeyBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more SSLCertKey records."""

    queryset = models.SSLCertKey.objects.all()
    table = tables.SSLCertKeyTable


class SSLCertKeyBulkImportView(generic.BulkImportView):
    """View for importing one or more SSLCertKey records."""

    queryset = models.SSLCertKey.objects.all()
    model_form = forms.SSLCertKeyCSVForm
    table = tables.SSLCertKeyTable


class SSLCertKeyBulkEditView(generic.BulkEditView):
    """View for editing one or more SSLCertKey records."""

    queryset = models.SSLCertKey.objects.all()
    table = tables.SSLCertKeyTable
    form = forms.SSLCertKeyBulkEditForm
