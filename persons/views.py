from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404

from .models import Document, Person
from .forms import PersonForm


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


def person_new(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            person.save()
            return redirect('person_detail', pk=person.pk)
    else:
        form = PersonForm()
    return render(request, "persons/person_edit.html", {"form": form})


def person_edit(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            person.save()
            return redirect('person_detail', pk=person.pk)
    else:
        form = PersonForm(instance=person)
    return render(request, "persons/person_edit.html", {"form": form})
