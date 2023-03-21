"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models
from nautobot.dcim.models import Site
from ..choices import ApplicationClassTypes, ApplicationAccessibility
from .utils import add_blank_choice


class CustomerForm(BootstrapMixin, forms.ModelForm):
    """Customer creation/edit form."""

    slug = AutoSlugField(populate_from=["name"])
    id = forms.CharField(label="ID")
    site = forms.ModelChoiceField(queryset=Site.objects.all(), label="Site")
    name = forms.CharField(label="Name")
    fqdn = forms.CharField(label="FQDN")
    oe = forms.CharField(abel="OE")
    email = forms.EmailField(abel="email")
    class_type = forms.ChoiceField(choices=add_blank_choice(ApplicationClassTypes))
    accessibility = forms.ChoiceField(choices=add_blank_choice(ApplicationClassTypes))
    test_url = forms.URLField(label="URL")

    class Meta:
        """Meta attributes."""

        model = models.Customer
        fields = ["slug", "id", "site", "name", "fqdn", "oe", "email", "class_type", "accessibility", "test_url"]


class CustomerFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = AutoSlugField(populate_from=["name"])
    id = forms.CharField(required=False, label="ID")
    site = forms.ModelChoiceField(queryset=Site.objects.all(), label="Site", required=False)
    name = forms.CharField(label="Name", required=False)
    fqdn = forms.CharField(label="FQDN", required=False)
    oe = forms.CharField(abel="OE", required=False)
    email = forms.EmailField(abel="email", required=False)
    class_type = forms.ChoiceField(choices=add_blank_choice(ApplicationClassTypes), required=False)
    accessibility = forms.ChoiceField(choices=add_blank_choice(ApplicationClassTypes), required=False)
    test_url = forms.URLField(required=False, label="URL")

    class Meta:
        """Meta attributes."""

        model = models.Customer
        fields = ["q", "slug", "id", "site", "name", "fqdn", "oe", "email", "class_type", "accessibility", "test_url"]


class CustomerBulkEditForm(BootstrapMixin, BulkEditForm):
    """Customer bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.Customer.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        nullable_fields = [
            "id",
        ]


class CustomerCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.Customer
        fields = models.Customer.csv_headers
