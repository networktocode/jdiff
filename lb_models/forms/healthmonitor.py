"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm, DynamicModelChoiceField
from nautobot.core.fields import AutoSlugField
from .utils import add_blank_choice
from lb_models import models

class VIPHealthMonitorForm(BootstrapMixin, forms.ModelForm):
    """VIP Health Monitor creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.VIPHealthMonitor
        fields = [
            "slug",
            "name",
            "description",
            "type",
            "url",
            "send",
            "code",
            "receive",
        ]


class VIPHealthMonitorFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    name = forms.CharField(required=False, label="Name")
    type = forms.CharField(required=False, label="Type")
    url = forms.URLField(required=False, label="URL")
    send = forms.CharField(required=False, label="Send")
    string = forms.CharField(required=False, label="String")
    code = forms.IntegerField(required=False, label="Code")
    receive = forms.CharField(required=False, label="Receive")

    class Meta:
        """Meta attributes."""

        model = models.VIPHealthMonitor
        fields = [
            "q",
            "slug",
            "name",
            "description",
            "type",
            "url",
            "send",
            "code",
            "receive",
        ]


class VIPHealthMonitorBulkEditForm(BootstrapMixin, BulkEditForm):
    """VIP Health Monitor bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.VIPHealthMonitor.objects.all(), widget=forms.MultipleHiddenInput)
    issuer = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.VIPHealthMonitor
        nullable_fields = [
            "name",
        ]


class VIPHealthMonitorCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.VIPHealthMonitor
        fields = models.VIPHealthMonitor.csv_headers
