"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models
from ..choices import MonitorTypes
from .utils import add_blank_choice


class MonitorForm(BootstrapMixin, forms.ModelForm):
    """Monitor creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])

    class Meta:
        """Meta attributes."""

        model = models.Monitor
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


class MonitorFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    name = forms.CharField(required=False, label="Name")
    description = forms.CharField(required=False, label="Description")
    type = forms.ChoiceField(choices=add_blank_choice(MonitorTypes), required=False)
    lrtm = forms.BooleanField(required=False, label="LRTM")
    secure = forms.BooleanField(required=False, label="Secure")
    url = forms.URLField(required=False, label="URL")
    send = forms.CharField(required=False, label="Send")
    string = forms.CharField(required=False, label="String")
    code = forms.IntegerField(label="Code")
    receive = forms.CharField(required=False, label="Receive")
    httprequest = forms.CharField(label="HTTP Request")

    class Meta:
        """Meta attributes."""

        model = models.Monitor
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


class MonitorBulkEditForm(BootstrapMixin, BulkEditForm):
    """Monitor bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.Monitor.objects.all(), widget=forms.MultipleHiddenInput)
    issuer = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.Monitor
        nullable_fields = [
            "name",
        ]


class MonitorCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.Monitor
        fields = models.Monitor.csv_headers
