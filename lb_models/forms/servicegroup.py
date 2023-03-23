"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models
from ..choices import ServiceGroupTypes
from .utils import add_blank_choice


class ServiceGroupForm(BootstrapMixin, forms.ModelForm):
    """Service Group Member creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    monitor = forms.ModelChoiceField(queryset=models.HealthMonitor.objects.all(), to_field_name="slug")
    member = forms.ModelChoiceField(queryset=models.ServiceGroupBinding.objects.all(), to_field_name="slug")

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        fields = ["slug", "name", "description", "monitor", "member", "type", "td", "sslprofile"]


class ServiceGroupFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = AutoSlugField(populate_from=["name"])
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    monitor = forms.ModelChoiceField(queryset=models.HealthMonitor.objects.all(), required=False, to_field_name="slug")
    member = forms.ModelChoiceField(
        queryset=models.ServiceGroupBinding.objects.all(), required=False, to_field_name="slug"
    )
    type = forms.ChoiceField(choices=add_blank_choice(ServiceGroupTypes), required=False)
    td = forms.BooleanField(required=False)
    sslprofile = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        fields = ["slug", "name", "description", "monitor", "member", "type", "td", "sslprofile"]


class ServiceGroupBulkEditForm(BootstrapMixin, BulkEditForm):
    """Certificate bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.ServiceGroup.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        nullable_fields = [
            "name",
        ]


class ServiceGroupCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        fields = models.ServiceGroup.csv_headers
