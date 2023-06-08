"""Views for ServiceGroup Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import servicegroup as forms


class ServiceGroupView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServiceGroup.objects.all()


class ServiceGroupListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServiceGroup.objects.all()
    filterset = filters.ServiceGroupFilterSet
    filterset_form = forms.ServiceGroupFilterForm
    table = tables.ServiceGroupTable
    action_buttons = ("import", "export", "add")


class ServiceGroupCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.ServiceGroup
    queryset = models.ServiceGroup.objects.all()
    model_form = forms.ServiceGroupForm


class ServiceGroupDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.ServiceGroup
    queryset = models.ServiceGroup.objects.all()


class ServiceGroupEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.ServiceGroup
    queryset = models.ServiceGroup.objects.all()
    model_form = forms.ServiceGroupBulkEditForm


class ServiceGroupBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServiceGroup records."""

    queryset = models.ServiceGroup.objects.all()
    table = tables.ServiceGroupTable


class ServiceGroupBulkImportView(generic.BulkImportView):
    """View for importing one or more ServiceGroup records."""

    queryset = models.ServiceGroup.objects.all()
    model_form = forms.ServiceGroupCSVForm
    table = tables.ServiceGroupTable


class ServiceGroupBulkEditView(generic.BulkEditView):
    """View for editing one or more ServiceGroup records."""

    queryset = models.ServiceGroup.objects.all()
    table = tables.ServiceGroupTable
    form = forms.ServiceGroupBulkEditForm
