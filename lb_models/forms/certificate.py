"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, DatePicker, CSVModelForm
from nautobot.core.fields import AutoSlugField
from ..choices import CertAlgorithmChoices
from .utils import add_blank_choice
from lb_models import models


class CertificateForm(BootstrapMixin, forms.ModelForm):
    """VIP Certificate creation/edit form."""

    slug = AutoSlugField(populate_from=["serial_number"])
    start_date = forms.DateField(widget=DatePicker())
    end_date = forms.DateField(widget=DatePicker())
    signature_algorithm = forms.ChoiceField(choices=add_blank_choice(CertAlgorithmChoices))
    subject_pub_key = forms.ChoiceField(choices=add_blank_choice(CertAlgorithmChoices))

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        fields = [
            "slug",
            "issuer",
            "version_number",
            "serial_number",
            "signature",
            "signature_algorithm",
            "signature_algorithm_id",
            "start_date",
            "end_date",
            "subject_name",
            "subject_pub_key",
            "subject_pub_key_algorithm",
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
    signature = forms.CharField(required=False, label="Signature")
    signature_algorithm = forms.ChoiceField(
        choices=add_blank_choice(CertAlgorithmChoices), required=False, label="Signature algorithm"
    )
    signature_algorithm_id = forms.CharField(required=False, label="Signature algorithm ID")
    start_date = forms.DateField(required=False, widget=DatePicker(), label="Start certificate date")
    end_date = forms.DateField(required=False, widget=DatePicker(), label="Expire certificate date")
    subject_name = forms.CharField(required=False, label="Subject name")
    subject_pub_key = forms.CharField(required=False, label="Subject pub key")
    subject_pub_key_algorithm = forms.ChoiceField(
        choices=add_blank_choice(CertAlgorithmChoices), required=False, label="Subject pub key algorithm"
    )

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        fields = [
            "q",
            "slug",
            "issuer",
            "serial_number",
            "signature",
            "signature_algorithm",
            "signature_algorithm_id",
            "start_date",
            "end_date",
            "subject_name",
            "subject_pub_key",
            "subject_pub_key_algorithm",
        ]


class CertificateBulkEditForm(BootstrapMixin, BulkEditForm):
    """VIP Certificate bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.Certificate.objects.all(), widget=forms.MultipleHiddenInput)
    issuer = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        nullable_fields = [
            "issuer",
        ]


class CertificateCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        fields = models.Certificate.csv_headers
