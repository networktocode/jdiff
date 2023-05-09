"""Forms for lb_models."""
from django import forms
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
from nautobot.core.fields import AutoSlugField
from lb_models import models
from nautobot.dcim.models import Site
from ..choices import ApplicationClassTypes, ApplicationAccessibility
from .utils import add_blank_choice


class CustomerAppProfileForm(BootstrapMixin, forms.ModelForm):
    """CustomerAppProfile creation/edit form."""

    slug = AutoSlugField(populate_from=["profile_name"])
    profile_name = forms.CharField(label="Profile Name")
    application_name = forms.CharField(label="Application Name")
    site = forms.ModelChoiceField(queryset=Site.objects.all(), label="Site")
    fqdn = forms.CharField(label="FQDN")
    oe_bu = forms.CharField(label="OE BU")
    owner_contact = forms.EmailField(label="Owner Contact")
    class_type = forms.ChoiceField(choices=add_blank_choice(ApplicationClassTypes))
    accessibility = forms.ChoiceField(choices=add_blank_choice(ApplicationAccessibility))
    test_url = forms.URLField(label="URL")

    class Meta:
        """Meta attributes."""

        model = models.CustomerAppProfile
        fields = [
            "slug",
            "profile_name",
            "application_name",
            "site",
            "fqdn",
            "oe_bu",
            "owner_contact",
            "class_type",
            "accessibility",
            "test_url",
        ]


class CustomerAppProfileFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within issuer or Slug.",
    )
    slug = AutoSlugField(populate_from=["profile_name"])
    profile_name = forms.CharField(required=False, label="Profile Name")
    application_name = forms.CharField(required=False, label="Application Name")
    site = forms.ModelChoiceField(queryset=Site.objects.all(), label="Site", required=False)
    fqdn = forms.CharField(label="FQDN", required=False)
    oe_bu = forms.CharField(label="OE BU", required=False)
    owner_contact = forms.EmailField(label="email", required=False)
    class_type = forms.ChoiceField(choices=add_blank_choice(ApplicationClassTypes), required=False)
    accessibility = forms.ChoiceField(choices=add_blank_choice(ApplicationAccessibility), required=False)
    test_url = forms.URLField(required=False, label="URL")

    class Meta:
        """Meta attributes."""

        model = models.CustomerAppProfile
        fields = [
            "q",
            "slug",
            "profile_name",
            "application_name",
            "site",
            "fqdn",
            "oe_bu",
            "owner_contact",
            "class_type",
            "accessibility",
            "test_url",
        ]


class CustomerAppProfileBulkEditForm(BootstrapMixin, BulkEditForm):
    """CustomerAppProfile bulk edit form."""

    pk = forms.ModelChoiceField(queryset=models.CustomerAppProfile.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        nullable_fields = [
            "id",
        ]


class CustomerAppProfileCSVForm(CSVModelForm):
    """Form for creating bulk Team."""

    class Meta:
        """Meta attributes."""

        model = models.CustomerAppProfile
        fields = models.CustomerAppProfile.csv_headers
