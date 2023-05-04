"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models
from nautobot.ipam.models import IPAddress, Interface, VLAN, VRF
from nautobot.dcim.models import Device
from ..choices import Protocols
from .utils import add_blank_choice


class VserverForm(BootstrapMixin, forms.ModelForm):
    """Vserver creation/edit form."""

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
    sslcertkey = forms.ModelChoiceField(queryset=models.SSLCertKey.objects.all(), label="SSLCertKey", required=False)
    owner = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.Vserver
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
            "sslcertkey",
            "owner",
        ]


class VserverFilterForm(BootstrapMixin, forms.ModelForm):
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
    sslcertkey = forms.ModelChoiceField(queryset=models.SSLCertKey.objects.all(), required=False, label="SSLCertKey")
    owner = forms.CharField(required=False, label="Owner")

    class Meta:
        """Meta attributes."""

        model = models.Vserver
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
            "sslcertkey",
            "owner",
        ]


class VserverBulkEditForm(BootstrapMixin, BulkEditForm):
    """Vserver bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.Vserver.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        nullable_fields = [
            "name",
        ]


class VserverCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.Vserver
        fields = models.Vserver.csv_headers
