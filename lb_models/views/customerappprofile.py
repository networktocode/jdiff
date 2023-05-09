"""Views for CustomerAppProfile Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import customerappprofile as forms


class CustomerAppProfileView(generic.ObjectView):
    """Detail view."""

    queryset = models.CustomerAppProfile.objects.all()


class CustomerAppProfileListView(generic.ObjectListView):
    """List view."""

    queryset = models.CustomerAppProfile.objects.all()
    filterset = filters.CustomerAppProfileFilterSet
    filterset_form = forms.CustomerAppProfileFilterForm
    table = tables.CustomerAppProfileTable
    action_buttons = ("import", "export", "add")


class CustomerAppProfileCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.CustomerAppProfile
    queryset = models.CustomerAppProfile.objects.all()
    model_form = forms.CustomerAppProfileForm


class CustomerAppProfileDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.CustomerAppProfile
    queryset = models.CustomerAppProfile.objects.all()


class CustomerAppProfileEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.CustomerAppProfile
    queryset = models.CustomerAppProfile.objects.all()
    model_form = forms.CustomerAppProfileForm


class CustomerAppProfileBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more CustomerAppProfile records."""

    queryset = models.CustomerAppProfile.objects.all()
    table = tables.CustomerAppProfileTable


class CustomerAppProfileBulkImportView(generic.BulkImportView):
    """View for importing one or more CustomerAppProfile records."""

    queryset = models.CustomerAppProfile.objects.all()
    model_form = forms.CustomerAppProfileCSVForm
    table = tables.CustomerAppProfileTable


class CustomerAppProfileBulkEditView(generic.BulkEditView):
    """View for editing one or more CustomerAppProfile records."""

    queryset = models.CustomerAppProfile.objects.all()
    table = tables.CustomerAppProfileTable
    form = forms.CustomerAppProfileForm
