"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models


class ServerServiceGroupBindingForm(BootstrapMixin, forms.ModelForm):
    """Service Group Member creation/edit form."""

    slug = AutoSlugField(populate_from=["group_server_name"])
    service_group = forms.ModelChoiceField(queryset=models.ServiceGroup.objects.all(), to_field_name="slug")

    class Meta:
        """Meta attributes."""

        model = models.ServerServiceGroupBinding
        fields = [
            "slug",
            "group_server_name",
            "service_group",
        ]


class ServerServiceGroupBindingFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    group_server_name = forms.CharField(required=False, label="Name")
    service_group = forms.ModelChoiceField(
        queryset=models.ServiceGroup.objects.all(), required=False, label="SG", to_field_name="slug"
    )

    class Meta:
        """Meta attributes."""

        model = models.ServerServiceGroupBinding
        fields = [
            "q",
            "slug",
            "group_server_name",
            "service_group",
        ]


class ServerServiceGroupBindingBulkEditForm(BootstrapMixin, BulkEditForm):
    """SSLCertKey bulk edit form."""

    pk = forms.ModelChoiceField(
        queryset=models.ServerServiceGroupBinding.objects.all(), widget=forms.MultipleHiddenInput
    )
    issuer = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServerServiceGroupBinding
        nullable_fields = [
            "group_server_name",
        ]


class ServerServiceGroupBindingCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.ServerServiceGroupBinding
        fields = models.ServerServiceGroupBinding.csv_headers
