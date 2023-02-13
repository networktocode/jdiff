"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm, DynamicModelChoiceField
from nautobot.core.fields import AutoSlugField
from ..choices import Protocols
from .utils import add_blank_choice
from lb_models import models

class VIPPoolForm(BootstrapMixin, forms.ModelForm):
    """VIP Pool Member creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    monitor = forms.ModelMultipleChoiceField(queryset=models.VIPHealthMonitor.objects.all(), required=False, to_field_name="slug")
    member = forms.ModelMultipleChoiceField(queryset=models.VIPPoolMember.objects.all(), required=False, to_field_name="slug")

    class Meta:
        """Meta attributes."""

        model = models.VIPPool
        fields = ["slug", "name", "description", "monitor", "member"]


class VIPPoolFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = AutoSlugField(populate_from=["name"])
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    monitor = forms.ModelMultipleChoiceField(queryset=models.VIPHealthMonitor.objects.all(), required=False, to_field_name="slug")
    member = forms.ModelMultipleChoiceField(queryset=models.VIPPoolMember.objects.all(), required=False, to_field_name="slug")

    class Meta:
        """Meta attributes."""

        model = models.VIPPool
        fields = ["slug", "name", "description", "monitor", "member"]



class VIPPoolBulkEditForm(BootstrapMixin, BulkEditForm):
    """VIP Certificate bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.VIPPool.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.VIPPool
        nullable_fields = [
            "name",
        ]


class VIPPoolCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.VIPPool
        fields = models.VIPPool.csv_headers
