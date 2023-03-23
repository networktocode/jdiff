"""Views for Certificate Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import certificate as forms


class CertificateView(generic.ObjectView):
    """Detail view."""

    queryset = models.Certificate.objects.all()


class CertificateListView(generic.ObjectListView):
    """List view."""

    queryset = models.Certificate.objects.all()
    filterset = filters.CertificateFilterSet
    filterset_form = forms.CertificateFilterForm
    table = tables.CertificateTable
    action_buttons = ("import", "export", "add")


class CertificateCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.Certificate
    queryset = models.Certificate.objects.all()
    model_form = forms.CertificateForm


class CertificateDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.Certificate
    queryset = models.Certificate.objects.all()


class CertificateEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.Certificate
    queryset = models.Certificate.objects.all()
    model_form = forms.CertificateForm


class CertificateBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Certificate records."""

    queryset = models.Certificate.objects.all()
    table = tables.CertificateTable


class CertificateBulkImportView(generic.BulkImportView):
    """View for importing one or more Certificate records."""

    queryset = models.Certificate.objects.all()
    model_form = forms.CertificateCSVForm
    table = tables.CertificateTable


class CertificateBulkEditView(generic.BulkEditView):
    """View for editing one or more Certificate records."""

    queryset = models.Certificate.objects.all()
    table = tables.CertificateTable
    form = forms.CertificateForm
