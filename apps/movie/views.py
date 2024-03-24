from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from itertools import chain


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
    template_name = 'movies/movies_list.html'

    if not settings.DEBUG:
        def get_queryset(self):
            filter_quality = self.request.GET.get("filter__movie-quality")
            search__movie = self.request.GET.get("search__movie")
            cache_key = "movies_list_key"
            queryset_from_cache = cache.get(cache_key)
            if not queryset_from_cache:
                queryset_from_cache = super().get_queryset()
                if filter_quality or search__movie:
                    queryset_from_cache = queryset_from_cache.filter(
                        Q(quality__name__icontains=filter_quality) |
                        Q(title__icontains=search__movie) |
                        Q(actors__icontains=search__movie)
                    )
                    if filter_quality:
                        queryset_from_cache = queryset_from_cache.filter(
                            quality__name__icontains=filter_quality)
                    if search__movie:
                        queryset_from_cache = queryset_from_cache.filter(
                            Q(title__icontains=search__movie) |
                            Q(actors__icontains=search__movie)
                        )
            return queryset_from_cache.order_by("-time_created")
    else:
        def get_queryset(self):
            queryset = super().get_queryset()
            filter_quality = self.request.GET.get("filter__movie-quality")
            search__movie = self.request.GET.get("search__movie")
            if filter_quality or search__movie:
                queryset = queryset.filter(
                    Q(quality__name__icontains=filter_quality) |
                    Q(title__icontains=search__movie) |
                    Q(actors__icontains=search__movie)
                )
                if filter_quality:
                    queryset = queryset.filter(
                        quality__name__icontains=filter_quality)
                if search__movie:
                    queryset = queryset.filter(
                        Q(title__icontains=search__movie) |
                        Q(actors__icontains=search__movie)
                    )
            return queryset.order_by("-time_created")

    def get_single_new_movie(self):
        calculate_2_day = timezone.now() - timedelta(days=2)
        calculate_movie_object = movie_models.Movie.objects.all().filter(
            time_created__gte=calculate_2_day)
        calculate_movie_object_ids = calculate_movie_object.values_list(
            "id", flat=True)
        all_movies = self.get_queryset().all()
        is_new_movie = [
            movies_id in calculate_movie_object_ids for movies_id in all_movies.values_list("id", flat=True)]
        return is_new_movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = entry_models.Category.objects.all()
        is_movie = self.get_single_new_movie()
        movies_queryset = self.get_queryset()
        combined_movies = [{"movie": movie, "is_new": is_new}
                           for movie, is_new in zip(movies_queryset, is_movie)]
        paginator = Paginator(combined_movies, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            movies = paginator.page(paginator.num_pages)

        context['movies'] = movies
        return context


# make classes to function names
movie_single = MovieSingle.as_view()
movies_list_view = MoviesListPage.as_view()
