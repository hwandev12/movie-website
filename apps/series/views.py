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
        serie = self.model.objects.get(id=self.kwargs.get("serieID", ""))
        
        request_episode = self.request.GET.get("season-number-got")
        if not request_episode:
            episodes = serie_models.Episode.objects.all().filter(series=serie)
        else:
            request_episode = int(request_episode)
            episodes = serie_models.Episode.objects.all().filter(series=serie, season_number=request_episode)
        context['categories'] = entry_models.Category.objects.all()
        context['episodes'] = episodes
        return context


# make name like function
serie_detail_view = SerieDetailView.as_view()
