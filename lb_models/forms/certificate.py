"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, DatePicker, CSVModelForm
from nautobot.core.fields import AutoSlugField
from .utils import add_blank_choice
from lb_models import models


class CertificateForm(BootstrapMixin, forms.ModelForm):
    """Certificate creation/edit form."""

    slug = AutoSlugField(populate_from=["serial_number"])
    start_date = forms.DateField(widget=DatePicker(), required=False)
    end_date = forms.DateField(widget=DatePicker(), required=False)
    certificate_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        fields = [
            "slug",
            "issuer",
            "version_number",
            "serial_number",
            "name",
            "certificate_key",
            "certificate_password",
            "start_date",
            "end_date",
        ]


class CertificateFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    issuer = forms.CharField(required=False, label="Issuer")
    serial_number = forms.CharField(required=False, label="SN")
    name = forms.CharField(required=False, label="Certificate Name")
    certificate_key = forms.CharField(required=False, label="Certificate Key")
    start_date = forms.DateField(required=False, widget=DatePicker(), label="Start certificate date")
    end_date = forms.DateField(required=False, widget=DatePicker(), label="Expire certificate date")


    class Meta:
        """Meta attributes."""

        model = models.Certificate
        fields = [
            "q",
            "slug",
            "issuer",
            "version_number",
            "serial_number",
            "name",
            "certificate_key",
            "start_date",
            "end_date",
        ]


class CertificateBulkEditForm(BootstrapMixin, BulkEditForm):
    """Certificate bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.Certificate.objects.all(), widget=forms.MultipleHiddenInput)
    certifcare = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        nullable_fields = [
            "name",
        ]


class CertificateCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        fields = models.Certificate.csv_headers
