from django.shortcuts import render
from django.views import generic
from . import models as serie_models
from apps.entry import models as entry_models


class SerieDetailView(generic.DetailView):
    model = serie_models.Series
    template_name = 'series/serie_detail.html'
    context_object_name = 'serie'
    pk_url_kwarg = 'serieID'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = entry_models.Category.objects.all()
        return context


# make name like function
serie_detail_view = SerieDetailView.as_view()
