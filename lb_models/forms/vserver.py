"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models
from ..choices import Methods
from .utils import add_blank_choice

class VserverForm(BootstrapMixin, forms.ModelForm):
    """Vserver creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    lb_method = forms.ChoiceField(choices=add_blank_choice(Methods), label="LB Method")
    ssl_binding = forms.ModelChoiceField(queryset=models.SSLCertKey.objects.all(), to_field_name="slug", label="SSL Binding")
    ssl_profile = forms.CharField(label="SSL Profile")
    snow_id = forms.CharField(label="SNOW ID")

    class Meta:
        """Meta attributes."""

        model = models.Vserver
        fields = [
            "slug",
            "name",
            "comment",
            "device",
            "ipv4_address",
            "service_group_binding",
            "service_type",
            "lb_method",
            "ssl_binding",
            "customer_app_profile",
            "ssl_profile",
            "persistence_type",
            "args",
            "snow_id",
        ]


class VserverFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = AutoSlugField(populate_from=["name"])

    class Meta:
        """Meta attributes."""

        model = models.Vserver
        fields = [
            "q",
            "slug",
            "name",
            "comment",
            "device",
            "ipv4_address",
            "service_group_binding",
            "service_type",
            "lb_method",
            "ssl_binding",
            "customer_app_profile",
            "ssl_profile",
            "persistence_type",
            "args",
            "snow_id",
        ]


class VserverBulkEditForm(BootstrapMixin, BulkEditForm):
    """Vserver bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.Vserver.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.Vserver
        nullable_fields = [
            "name",
        ]


class VserverCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.Vserver
        fields = models.Vserver.csv_headers
