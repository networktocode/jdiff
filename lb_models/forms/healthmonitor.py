"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models
from ..choices import HealthMonitorTypes
from .utils import add_blank_choice


class HealthMonitorForm(BootstrapMixin, forms.ModelForm):
    """Health Monitor creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])

    class Meta:
        """Meta attributes."""

        model = models.HealthMonitor
        fields = [
            "slug",
            "name",
            "description",
            "type",
            "lrtm",
            "secure",
            "url",
            "send",
            "code",
            "receive",
            "httprequest",
        ]


class HealthMonitorFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    name = forms.CharField(required=False, label="Name")
    description = forms.CharField(required=False, label="Description")
    type = forms.ChoiceField(choices=add_blank_choice(HealthMonitorTypes), required=False)
    lrtm = forms.BooleanField(required=False, label="LRTM")
    secure = forms.BooleanField(required=False, label="Secure")
    url = forms.URLField(required=False, label="URL")
    send = forms.CharField(required=False, label="Send")
    string = forms.CharField(required=False, label="String")
    code = forms.IntegerField(required=False, label="Code")
    receive = forms.CharField(required=False, label="Receive")
    httprequest = forms.CharField(required=False, label="HTTP Request")

    class Meta:
        """Meta attributes."""

        model = models.HealthMonitor
        fields = [
            "q",
            "slug",
            "name",
            "description",
            "type",
            "lrtm",
            "secure",
            "url",
            "send",
            "code",
            "receive",
            "httprequest",
        ]


class HealthMonitorBulkEditForm(BootstrapMixin, BulkEditForm):
    """Health Monitor bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.HealthMonitor.objects.all(), widget=forms.MultipleHiddenInput)
    issuer = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.HealthMonitor
        nullable_fields = [
            "name",
        ]


class HealthMonitorCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.HealthMonitor
        fields = models.HealthMonitor.csv_headers
