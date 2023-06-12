"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm, StaticSelect2
from nautobot.core.fields import AutoSlugField
from lb_models import models
from nautobot.ipam.models import IPAddress
from .utils import add_blank_choice


class ServerForm(BootstrapMixin, forms.ModelForm):
    """Server creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    ipv4_address = forms.ModelChoiceField(queryset=IPAddress.objects.all(), label="IPv4 Address")
    td = forms.IntegerField(label="TD")
    state = forms.BooleanField(
        widget=forms.Select(
            choices=((False, "DISABLED"), (True, "ENABLED")),
        ),
        initial=False,
        required=False,
        label="Server",
    )

    class Meta:
        """Meta attributes."""

        model = models.Server
        fields = ["slug", "name", "state", "ipv4_address", "td", "snow_ticket_id"]


class ServerFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = AutoSlugField(populate_from=["name"])
    state = forms.CharField(required=False, label="State")
    name = forms.CharField(required=False, label="Name")
    ipv4_address = forms.ModelChoiceField(queryset=IPAddress.objects.all(), label="IP Address", required=False)
    td = forms.IntegerField(required=False, label="TD")

    class Meta:
        """Meta attributes."""

        model = models.Server
        fields = [
            "q",
            "slug",
            "name",
            "state",
            "ipv4_address",
            "td",
        ]


class ServerBulkEditForm(BootstrapMixin, BulkEditForm):
    """Server bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.Server.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.Server
        nullable_fields = [
            "name",
        ]


class ServerCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.Server
        fields = models.Server.csv_headers
