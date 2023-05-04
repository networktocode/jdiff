"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from ..choices import Protocols
from .utils import add_blank_choice
from lb_models import models
from nautobot.ipam.models import IPAddress


class ServiceGroupMonitorBindingForm(BootstrapMixin, forms.ModelForm):
    """Service Group Member creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    service_group = forms.ModelChoiceField(queryset=models.ServiceGroup.objects.all(), to_field_name="slug")
    monitor = forms.ModelChoiceField(queryset=models.Monitor.objects.all(), to_field_name="slug")

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupMonitorBinding
        fields = [
            "slug",
            "name",
            "monitor",
            "service_group",
        ]


class ServiceGroupMonitorBindingFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    name = forms.CharField(required=False, label="Name")
    monitor = forms.ModelChoiceField(
        queryset=models.Monitor.objects.all(), required=False, label="Monitor", to_field_name="slug"
    )
    service_group = forms.ModelChoiceField(
        queryset=models.ServiceGroup.objects.all(), required=False, label="Monitor", to_field_name="slug"
    )
    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupMonitorBinding
        fields = [
            "q",
            "slug",
            "name",
            "monitor",
            "service_group",
        ]


class ServiceGroupMonitorBindingBulkEditForm(BootstrapMixin, BulkEditForm):
    """SSLCertKey bulk edit form."""

    pk = forms.ModelChoiceField(
        queryset=models.ServiceGroupMonitorBinding.objects.all(), widget=forms.MultipleHiddenInput
    )
    issuer = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupMonitorBinding
        nullable_fields = [
            "name",
        ]


class ServiceGroupMonitorBindingCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupMonitorBinding
        fields = models.ServiceGroupMonitorBinding.csv_headers
