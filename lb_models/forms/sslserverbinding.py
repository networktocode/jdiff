"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, DatePicker, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models


class SSLServerBindingForm(BootstrapMixin, forms.ModelForm):
    """SSLServerBinding creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """Meta attributes."""

        model = models.SSLServerBinding
        fields = [
            "slug",
            "name",
            "ssl_certkey",
        ]


class SSLServerBindingFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = forms.CharField(required=False, label="Slug")
    name = forms.CharField(required=False, label="SSL Server Binding Name")
    ssl_certkey = forms.CharField(required=False, label="SSL Cert Key")

    class Meta:
        """Meta attributes."""

        model = models.SSLServerBinding
        fields = [
            "q",
            "slug",
            "name",
            "ssl_certkey",
        ]


class SSLServerBindingBulkEditForm(BootstrapMixin, BulkEditForm):
    """SSLServerBinding bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.SSLServerBinding.objects.all(), widget=forms.MultipleHiddenInput)

    class Meta:
        """Meta attributes."""

        model = models.SSLServerBinding
        nullable_fields = [
            "name",
        ]


class SSLServerBindingCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.SSLServerBinding
        fields = models.SSLServerBinding.csv_headers
