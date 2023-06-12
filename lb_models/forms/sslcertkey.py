"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, DatePicker, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models


class SSLCertKeyForm(BootstrapMixin, forms.ModelForm):
    """SSLCertKey creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    snow_ticket_id = forms.CharField(label="SNOW ID")

    class Meta:
        """Meta attributes."""

        model = models.SSLCertKey
        fields = [
            "slug",
            "key_name",
            "private_key_filename",
            "private_crt_filename",
            "key_password",
            "snow_ticket_id",
        ]


class SSLCertKeyFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    key_name = forms.CharField(required=False, label="Key Name")
    private_key_filename = forms.CharField(required=False, label="Key Filename")
    private_crt_filename = forms.CharField(required=False, label="Cert Filename")
    snow_ticket_id = forms.CharField(required=False, label="SNOW ID")

    class Meta:
        """Meta attributes."""

        model = models.SSLCertKey
        fields = [
            "q",
            "slug",
            "key_name",
            "private_key_filename",
            "private_crt_filename",
            "snow_ticket_id",
        ]


class SSLCertKeyBulkEditForm(BootstrapMixin, BulkEditForm):
    """SSLCertKey bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.SSLCertKey.objects.all(), widget=forms.MultipleHiddenInput)

    class Meta:
        """Meta attributes."""

        model = models.SSLCertKey
        nullable_fields = [
            "key_name",
        ]


class SSLCertKeyCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.SSLCertKey
        fields = models.SSLCertKey.csv_headers
