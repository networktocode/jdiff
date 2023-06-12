"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm, StaticSelect2
from nautobot.core.fields import AutoSlugField
from lb_models import models
from ..choices import MonitorTypes
from .utils import add_blank_choice


class MonitorForm(BootstrapMixin, forms.ModelForm):
    """Monitor creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    lrtm = forms.BooleanField(
        widget=forms.Select(
            choices=((False, "DISABLED"), (True, "ENABLED")),
        ),
        initial=False,
        required=False,
        label="LRTM",
    )
    snow_ticket_id = forms.CharField(label="SNOW ID")

    class Meta:
        """Meta attributes."""

        model = models.Monitor
        fields = ["slug", "name", "comment", "type", "lrtm", "args", "snow_ticket_id"]


class MonitorFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    name = forms.CharField(required=False, label="Name")
    comment = forms.CharField(required=False, label="Comment")
    type = forms.ChoiceField(choices=add_blank_choice(MonitorTypes), required=False)
    lrtm = forms.NullBooleanField(
        required=False, widget=StaticSelect2(choices=add_blank_choice((("ENABLED", "yes"), ("DISABLED", "no"))))
    )
    snow_ticket_id = forms.CharField(required=False, label="SNOW ID")

    class Meta:
        """Meta attributes."""

        model = models.Monitor
        fields = ["q", "slug", "name", "comment", "type", "lrtm", "args", "snow_ticket_id"]


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
