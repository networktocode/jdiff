"""Views for VIPCertificate Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import certificates as forms


class VIPCertificateView(generic.ObjectView):
    """Detail view."""

    queryset = models.VIPCertificate.objects.all()


class VIPCertificateListView(generic.ObjectListView):
    """List view."""

    queryset = models.VIPCertificate.objects.all()
    filterset = filters.VIPCertificateFilterSet
    filterset_form = forms.VIPCertificateFilterForm
    table = tables.VIPCertificateTable
    action_buttons = ("import", "export", "add")


class VIPCertificateCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.VIPCertificate
    queryset = models.VIPCertificate.objects.all()
    model_form = forms.VIPCertificateForm


class VIPCertificateDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.VIPCertificate
    queryset = models.VIPCertificate.objects.all()


class VIPCertificateEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.VIPCertificate
    queryset = models.VIPCertificate.objects.all()
    model_form = forms.VIPCertificateForm


class VIPCertificateBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more VIPCertificate records."""

    queryset = models.VIPCertificate.objects.all()
    table = tables.VIPCertificateTable


class VIPCertificateBulkImportView(generic.BulkImportView):
    """View for importing one or more VIPCertificate records."""

    queryset = models.VIPCertificate.objects.all()
    model_form = forms.VIPCertificateCSVForm
    table = tables.VIPCertificateTable


class VIPCertificateBulkEditView(generic.BulkEditView):
    """View for editing one or more VIPCertificate records."""

    queryset = models.VIPCertificate.objects.all()
    table = tables.VIPCertificateTable
    form = forms.VIPCertificateForm
