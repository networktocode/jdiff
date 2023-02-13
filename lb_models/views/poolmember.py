"""Views for VIPPoolMember Calendar."""
from nautobot.core.views import generic

from lb_models import filters, models, tables
from lb_models.forms import poolmember as forms


class VIPPoolMemberView(generic.ObjectView):
    """Detail view."""

    queryset = models.VIPPoolMember.objects.all()


class VIPPoolMemberListView(generic.ObjectListView):
    """List view."""

    queryset = models.VIPPoolMember.objects.all()
    filterset = filters.VIPPoolMemberFilterSet
    filterset_form = forms.VIPPoolMemberFilterForm
    table = tables.VIPPoolMemberTable
    action_buttons = ("import", "export", "add")


class VIPPoolMemberCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.VIPPoolMember
    queryset = models.VIPPoolMember.objects.all()
    model_form = forms.VIPPoolMemberForm


class VIPPoolMemberDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.VIPPoolMember
    queryset = models.VIPPoolMember.objects.all()


class VIPPoolMemberEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.VIPPoolMember
    queryset = models.VIPPoolMember.objects.all()
    model_form = forms.VIPPoolMemberForm


class VIPPoolMemberBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more VIPPoolMember records."""

    queryset = models.VIPPoolMember.objects.all()
    table = tables.VIPPoolMemberTable


class VIPPoolMemberBulkImportView(generic.BulkImportView):
    """View for importing one or more VIPPoolMember records."""

    queryset = models.VIPPoolMember.objects.all()
    model_form = forms.VIPPoolMemberCSVForm
    table = tables.VIPPoolMemberTable


class VIPPoolMemberBulkEditView(generic.BulkEditView):
    """View for editing one or more VIPPoolMember records."""

    queryset = models.VIPPoolMember.objects.all()
    table = tables.VIPPoolMemberTable
    form = forms.VIPPoolMemberForm
