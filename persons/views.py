from django.views.generic import DetailView, ListView

from .models import Document, Person


class PersonListView(ListView):
    """
    ListView for Person`s model

    Return querysets all persons with related document (passport).
    """

    model = Person
    template_name = "persons/person_full.html"
    context_object_name = 'persons'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["documents"] = Document.objects.filter(
            type_of_document="Passport")
        return context


class PersonDetailView(DetailView):
    """Detail view for Person`s model"""

    model = Person
    template_name = "persons/person_detail.html"
