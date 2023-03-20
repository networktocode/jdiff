"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models
from nautobot.ipam.models import IPAddress, Interface, VLAN, VRF
from nautobot.dcim.models import Device
from ..choices import Protocols
from .utils import add_blank_choice


class vserverForm(BootstrapMixin, forms.ModelForm):
    """vserver creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    description = forms.CharField(required=False)
    device = forms.ModelChoiceField(queryset=Device.objects.all(), label="Device")
    interface = forms.ModelChoiceField(queryset=Interface.objects.all(), label="Interface")
    address = forms.ModelChoiceField(queryset=IPAddress.objects.all(), label="IPv4 Address")
    pool = forms.ModelChoiceField(queryset=models.ServiceGroup.objects.all(), label="Service Group")
    vlan = forms.ModelChoiceField(queryset=VLAN.objects.all(), label="VLAN", required=False)
    vrf = forms.ModelChoiceField(queryset=VRF.objects.all(), label="VRF", required=False)
    fqdn = forms.CharField(required=False)
    protocol = forms.ChoiceField(choices=add_blank_choice(Protocols))
    method = forms.CharField(required=False)
    certificate = forms.ModelChoiceField(queryset=models.Certificate.objects.all(), label="Certificate", required=False)
    owner = forms.CharField(required=False)
    vserver_args = forms.JSONField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.vserver
        fields = [
            "slug",
            "name",
            "description",
            "device",
            "interface",
            "address",
            "pool",
            "vlan",
            "vrf",
            "fqdn",
            "protocol",
            "port",
            "method",
            "certificate",
            "owner",
            "vserver_args",
        ]


class vserverFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = AutoSlugField(populate_from=["name"])
    description = forms.CharField(required=False, label="Description")
    name = forms.CharField(required=False, label="Name")
    port = forms.IntegerField(required=False, label="Port")
    device = forms.ModelChoiceField(queryset=Device.objects.all(), label="Device", required=False)
    address = forms.ModelChoiceField(queryset=IPAddress.objects.all(), label="IP Address", required=False)
    pool = forms.ModelChoiceField(queryset=models.ServiceGroup.objects.all(), label="Service Group", required=False)
    vlan = forms.ModelChoiceField(queryset=VLAN.objects.all(), label="VLAN", required=False)
    vrf = forms.ModelChoiceField(queryset=VRF.objects.all(), label="VRF", required=False)
    fqdn = forms.CharField(required=False, label="FQDN")
    protocol = forms.ChoiceField(choices=add_blank_choice(Protocols), required=False, label="Protocol")
    method = forms.CharField(required=False, label="Method")
    certificate = forms.ModelChoiceField(queryset=models.Certificate.objects.all(), required=False, label="Certificate")
    owner = forms.CharField(required=False, label="Owner")

    class Meta:
        """Meta attributes."""

        model = models.vserver
        fields = [
            "q",
            "slug",
            "name",
            "description",
            "device",
            "address",
            "pool",
            "vlan",
            "vrf",
            "fqdn",
            "protocol",
            "port",
            "method",
            "certificate",
            "owner",
        ]


class vserverBulkEditForm(BootstrapMixin, BulkEditForm):
    """vserver bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.vserver.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        nullable_fields = [
            "name",
        ]


class vserverCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.vserver
        fields = models.vserver.csv_headers
