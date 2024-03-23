from typing import Any
from django.shortcuts import render
from django.views import generic
from django.core.cache.utils import make_template_fragment_key
from django.core.cache import cache
from django.db.models import Q

from . import models as serie_models
from apps.entry import models as entry_models


class SerieDetailView(generic.DetailView):
    model = serie_models.Series
    template_name = 'series/serie_detail.html'
    context_object_name = 'serie'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """
        Agar qo'yilayogan serial barcha qismlar deb qo'ysa unda 
        fasllarni tanlay oladigon bo'lishi kerak
        """
        context = super().get_context_data(**kwargs)
        serie = self.model.objects.get(slug=self.kwargs.get("slug", ""))
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
        if full_path == f'/series/single-movie/{self.kwargs.get("slug", "")}/':
            is_main_tag_home = True
        context['is_main_tag_home'] = is_main_tag_home
        context['full_path'] = full_path
        context['serie_id'] = serie_id
        return context


class EpisodeWatch(generic.DetailView):
    model = serie_models.Episode
    template_name = 'series/watch.html'
    context_object_name = 'episode'
    pk_url_kwarg = 'episodeID'

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug", "")
        episodeID = self.kwargs.get("episodeID", "")
        serie = serie_models.Series.objects.get(slug=slug)
        queryset = self.model.objects.filter(id=episodeID, series=serie)
        obj = queryset.first()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        serie = serie_models.Series.objects.get(slug=self.kwargs.get("slug", ""))
        season_number = []
        episodes = serie_models.Episode.objects.all().filter(series=serie)

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
        context['serie'] = serie_models.Series.objects.get(
            slug=self.kwargs.get("slug", ""))
        context['episodes'] = episodes
        is_main_tag_home = False
        serie_id = str(serie.id)
        full_path = self.request.get_full_path()
        if full_path == f'/series/single-movie/{self.kwargs.get("slug", "")}/{self.kwargs.get("episodeID")}/':
            is_main_tag_home = True
        context['is_main_tag_home'] = is_main_tag_home
        context['full_path'] = full_path
        context['serie_id'] = serie_id
        return context
    
class SeriesListPage(generic.ListView):
    paginate_by = 10
    model = serie_models.Series
    context_object_name = 'series'
    template_name = 'series/series_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_quality = self.request.GET.get("filter__movie-quality")
        search__movie = self.request.GET.get("search__movie")
        cache_key = make_template_fragment_key("series_list_key")
        if filter_quality or search__movie:
            queryset = queryset.filter(
                Q(quality__name__icontains=filter_quality) |
                Q(title__icontains=search__movie) |
                Q(actors__icontains=search__movie)
            )
            if filter_quality:
                queryset = queryset.filter(quality__name__icontains=filter_quality)
            if search__movie:
                queryset = queryset.filter(
                    Q(title__icontains=search__movie) |
                    Q(actors__icontains=search__movie)
                )
            cache.delete(cache_key)
        cache.delete(cache_key)
        return queryset.order_by("-time_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = entry_models.Category.objects.all()
        return context


# make name like function
serie_detail_view = SerieDetailView.as_view()
episode_watch = EpisodeWatch.as_view()
series_list_view = SeriesListPage.as_view()

