from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from . import models
from apps.entry import models as entry_models
from apps.movie import models as movie_models
from apps.series import models as serie_models

import json


class MovieSingle(generic.DetailView):
    model = models.Movie
    template_name = 'movies/single_movie.html'
    context_object_name = 'movie'
    pk_url_kwarg = 'movieID'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = entry_models.Category.objects.all()
        return context


def get_single_video(request, ID):
    is_movie = request.GET.get("is_movie")
    if is_movie == 'movie':
        movie = movie_models.Movie.objects.get(id=ID)
        trailer = movie_models.Trailer.objects.get(movie=movie)
        movie = serializers.serialize('json', [movie])
        trailer = serializers.serialize("json", [trailer])
        data = {"id": ID, "movie_ajax": movie, "trailer_ajax": trailer}
        return JsonResponse(data, safe=False)
    else:
        serie = serie_models.Series.objects.get(id=ID)
        serie_trailer = serie_models.SeriesTrailer.objects.get(movie=serie)
        serie = serializers.serialize('json', [serie])
        serie_trailer = serializers.serialize("json", [serie_trailer])
        data = {"id": ID, "serie_ajax": serie, "serie_trailer": serie_trailer}
        return JsonResponse(data, safe=False)


class MoviesListPage(generic.ListView):
    paginate_by = 10
    model = movie_models.Movie
    context_object_name = 'movies'
    template_name = 'movies/movies_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_quality = self.request.GET.get("filter__movie-quality")
        search__movie = self.request.GET.get("search__movie")
        cache_key = make_template_fragment_key("movies_list_key")
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

# make classes to function names
movie_single = MovieSingle.as_view()
movies_list_view = MoviesListPage.as_view()