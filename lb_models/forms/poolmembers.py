"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, DatePicker, CSVModelForm
from nautobot.core.fields import AutoSlugField
from ..choices import CertAlgorithmChoices, Protocols
from .utils import add_blank_choice
from lb_models import models


class VIPPoolMembersForm(BootstrapMixin, forms.ModelForm):
    """VIP Pool Members creation/edit form."""

    slug = AutoSlugField(populate_from=["serial_number"])
    start_date = forms.DateField(widget=DatePicker())
    end_date = forms.DateField(widget=DatePicker())
    signature_algorithm = forms.ChoiceField(choices=add_blank_choice(CertAlgorithmChoices))
    subject_pub_key = forms.ChoiceField(choices=add_blank_choice(CertAlgorithmChoices))

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
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


class VIPPoolMemberFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    name = forms.CharField(required=False, label="Name")
    description = forms.CharField(required=False, label="Description")
    protocol = forms.ChoiceField(
        choices=add_blank_choice(Protocols), required=False, label="Protocol"
    )
    port = forms.IntegerField(required=False, label="Port")
    ipv4_address = forms.GenericIPAddressField(required=False, label="IPv4/IPv6 address")
    fqnd = forms.URLField(required=False, label="FQDN")
    monitor = forms.ModelMultipleChoiceField(queryset=models.VIPHealthMonitor.objects.all(), required=False, to_field_name="slug")
    member_args = forms.JSONField(required=False, label="Extra member arguments")


    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
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


class VIPPoolMemberBulkEditForm(BootstrapMixin, BulkEditForm):
    """VIP Certificate bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.VIPPoolMember.objects.all(), widget=forms.MultipleHiddenInput)
    issuer = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
        nullable_fields = [
            "issuer",
        ]


class VIPPoolMemberCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
        fields = models.VIPPoolMember.csv_headers
