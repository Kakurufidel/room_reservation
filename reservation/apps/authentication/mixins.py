from django.views.generic import ListView
from django.http import HttpResponseForbidden


class AdminRequiredMixin:
    """
    Vérifie si l'utilisateur est un administrateur avant d'afficher la vue.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class PaginatedListView(ListView):
    """
    Vue générique avec pagination pour les listes d'objets.
    """

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get("page")
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        context["page_obj"] = paginator.get_page(page_number)
        return context
