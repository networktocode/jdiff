"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from ..choices import Protocols
from .utils import add_blank_choice
from lb_models import models
from nautobot.ipam.models import IPAddress


class VIPPoolMemberForm(BootstrapMixin, forms.ModelForm):
    """VIP Pool Member creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    description = forms.CharField(required=False)
    protocol = forms.ChoiceField(choices=add_blank_choice(Protocols))
    address = forms.ModelChoiceField(queryset=IPAddress.objects.all())
    monitor = forms.ModelChoiceField(queryset=models.HealthMonitor.objects.all(), to_field_name="slug")
    member_args = forms.JSONField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
        fields = [
            "slug",
            "name",
            "description",
            "protocol",
            "port",
            "address",
            "fqdn",
            "monitor",
            "member_args",
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
    protocol = forms.ChoiceField(choices=add_blank_choice(Protocols), required=False, label="Protocol")
    port = forms.IntegerField(required=False, label="Port")
    address = forms.ModelChoiceField(queryset=IPAddress.objects.all(), label="IP address")
    fqnd = forms.CharField(required=False, label="FQDN")
    monitor = forms.ModelChoiceField(
        queryset=models.HealthMonitor.objects.all(), required=False, label="Healt Monitor", to_field_name="slug"
    )

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
        fields = [
            "q",
            "slug",
            "name",
            "description",
            "protocol",
            "port",
            "address",
            "fqdn",
            "monitor",
        ]


class VIPPoolMemberBulkEditForm(BootstrapMixin, BulkEditForm):
    """Certificate bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.VIPPoolMember.objects.all(), widget=forms.MultipleHiddenInput)
    issuer = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
        nullable_fields = [
            "name",
        ]


class VIPPoolMemberCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
        fields = models.VIPPoolMember.csv_headers
