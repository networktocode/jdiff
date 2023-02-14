"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm, DynamicModelChoiceField
from nautobot.core.fields import AutoSlugField
from lb_models import models
from nautobot.ipam.models import IPAddress, Interface, VLAN, VRF
from nautobot.dcim.models import Device
from ..choices import Protocols
from .utils import add_blank_choice


class VIPForm(BootstrapMixin, forms.ModelForm):
    """VIP creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    description = forms.CharField(required=False)
    device = DynamicModelChoiceField(queryset=Device.objects.all(), label="Device")
    interface = DynamicModelChoiceField(queryset=Interface.objects.all(), label="Interface")
    ipv4_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), label="IPv4 Address")
    ipv6_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), label="IPv6 Address", required=False)
    pool = DynamicModelChoiceField(queryset=models.VIPPool.objects.all(), label="VIP Pool")
    vlan = DynamicModelChoiceField(queryset=VLAN.objects.all(), label="VLAN", required=False)
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), label="VRF", required=False)
    fqdn = forms.URLField(required=False)
    protocol = forms.ChoiceField(choices=add_blank_choice(Protocols))
    method = forms.CharField(required=False)
    certificate = DynamicModelChoiceField(queryset=models.VIPCertificate.objects.all(), label="VIP Pool")
    owner = forms.CharField(required=False)
    vip_args = forms.JSONField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.VIP
        fields = [
            "slug",
            "name",
            "description",
            "device",
            "interface",
            "ipv4_address",
            "ipv6_address",
            "pool",
            "vlan",
            "vrf",
            "fqdn",
            "protocol",
            "port",
            "method",
            "certificate",
            "owner",
            "vip_args",
        ]


class VIPFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = AutoSlugField(populate_from=["name"])
    description = forms.CharField(required=False)
    device = DynamicModelChoiceField(queryset=Device.objects.all(), label="Device")
    interface = DynamicModelChoiceField(queryset=Interface.objects.all(), label="Interface")
    ipv4_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), label="IPv4 Address")
    ipv6_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), label="IPv6 Address", required=False)
    pool = DynamicModelChoiceField(queryset=models.VIPPool.objects.all(), label="VIP Pool")
    vlan = DynamicModelChoiceField(queryset=VLAN.objects.all(), label="VLAN", required=False)
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), label="VRF", required=False)
    fqdn = forms.URLField(required=False)
    protocol = forms.ChoiceField(choices=add_blank_choice(Protocols))
    method = forms.CharField(required=False)
    certificate = DynamicModelChoiceField(queryset=models.VIPCertificate.objects.all(), label="VIP Pool")
    owner = forms.CharField(required=False)
    vip_args = forms.JSONField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.VIP
        fields = [
            "q",
            "slug",
            "name",
            "description",
            "device",
            "interface",
            "ipv4_address",
            "ipv6_address",
            "pool",
            "vlan",
            "vrf",
            "fqdn",
            "protocol",
            "port",
            "method",
            "certificate",
            "owner",
            "vip_args",
        ]

class VIPBulkEditForm(BootstrapMixin, BulkEditForm):
    """VIP bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.VIP.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.VIPPool
        nullable_fields = [
            "name",
        ]


class VIPCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.VIP
        fields = models.VIP.csv_headers
