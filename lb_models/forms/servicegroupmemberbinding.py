"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models


class ServiceGroupMemberBindingForm(BootstrapMixin, forms.ModelForm):
    """Service Group Member creation/edit form."""

    slug = AutoSlugField(populate_from=["group_binding_name"])
    server_name = forms.ModelChoiceField(queryset=models.Server.objects.all(), to_field_name="slug")

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupMemberBinding
        fields = [
            "slug",
            "group_binding_name",
            "server_name",
            "server_port",
        ]


class ServiceGroupMemberBindingFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    group_binding_name = forms.CharField(required=False, label="Service Group Binding Name")
    server_port = forms.IntegerField(required=False, label="Port")
    server_name = forms.ModelChoiceField(queryset=models.Server.objects.all(), label="Server Name")

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupMemberBinding
        fields = [
            "q",
            "slug",
            "group_binding_name",
            "server_port",
            "server_name",
        ]


class ServiceGroupMemberBindingBulkEditForm(BootstrapMixin, BulkEditForm):
    """Bulk edit form."""

    pk = forms.ModelChoiceField(
        queryset=models.ServiceGroupMemberBinding.objects.all(), widget=forms.MultipleHiddenInput
    )

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupMemberBinding
        nullable_fields = [
            "group_binding_name",
        ]


class ServiceGroupMemberBindingCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupMemberBinding
        fields = models.ServiceGroupMemberBinding.csv_headers
