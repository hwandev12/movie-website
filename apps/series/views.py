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
        """
        Agar qo'yilayogan serial barcha qismlar deb qo'ysa unda 
        fasllarni tanlay oladigon bo'lishi kerak
        """
        context = super().get_context_data(**kwargs)
        serie = self.model.objects.get(id=self.kwargs.get("serieID", ""))
        season_number = []
        episodes = serie_models.Episode.objects.all().filter(series=serie)
        first_episode = serie_models.Episode.objects.filter(
            series=serie).first()

        for e in episodes:
            v_list = e.season_number
            season_number.append(v_list)

        request_episode = self.request.GET.get("season-number-got")
        if not request_episode:
            episodes = serie_models.Episode.objects.all().filter(series=serie, season_number=1)
        else:
            request_episode = int(request_episode)
            episodes = serie_models.Episode.objects.all().filter(
                series=serie, season_number=request_episode)
        context['season_number'] = tuple(set(season_number))[1:]
        context['request_episode'] = request_episode
        context['categories'] = entry_models.Category.objects.all()
        context['episodes'] = episodes
        context['first_episode'] = first_episode
        is_main_tag_home = False
        serie_id = str(serie.id)
        full_path = self.request.get_full_path()
        if full_path == f'/series/single-movie/{serie_id}/':
            is_main_tag_home = True
        context['is_main_tag_home'] = is_main_tag_home
        context['full_path'] = full_path
        context['serie_id'] = serie_id
        return context


# make name like function
serie_detail_view = SerieDetailView.as_view()
