from django.views import generic
from itertools import chain
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from django.conf import settings
from django_countries.fields import CountryIContains


from apps.entry import models as entry_models
from apps.movie import models as movie_models
from apps.series import models as serie_models


class SearchPage(generic.TemplateView):
    template_name = 'search/search_film.html'
    paginate_by = 12

    def search(self):
        calculate_2_day = timezone.now() - timedelta(days=2)
        movies = movie_models.Movie.objects.all().order_by("-time_created")
        series = serie_models.Series.objects.all().order_by("-time_created")
        all_films = list((chain(movies, series)))
        if self.request.method == 'GET':
            search_film = self.request.GET.get("search__all_films")
            new_films_filter = self.request.GET.get("new_films_filter")
            film_filter_by_janr = self.request.GET.get("filter_movies")
            if search_film:
                found_movies = movies.filter(
                    Q(title__icontains=search_film) |
                    Q(actors__icontains=search_film)
                )
                found_series = series.filter(
                    Q(title__icontains=search_film) |
                    Q(actors__icontains=search_film)
                )
                all_films = list(chain(found_movies, found_series))
            elif new_films_filter == 'new':
                found_movies = movies.filter(
                    time_created__gte=calculate_2_day
                )
                found_series = series.filter(
                    time_created__gte=calculate_2_day
                )
                all_films = list(chain(found_movies, found_series))
            elif film_filter_by_janr:
                found_movies = movies.filter(
                    Q(countries__icontains=film_filter_by_janr) |
                    Q(genre__name__contains=film_filter_by_janr)
                ).distinct()
                
                found_series = series.filter(
                    Q(countries__icontains=film_filter_by_janr) |
                    Q(genre__name__icontains=film_filter_by_janr)
                ).distinct()
                
                all_films = list(chain(found_movies, found_series))
            else:
                all_films = sorted(
                    chain(movies, series),
                    key=lambda x: x.time_created,
                    reverse=True
                )
        return all_films

    @staticmethod
    def get_new_added_films():
        all_movies = movie_models.Movie.objects.all().order_by("-time_created")
        all_series = serie_models.Series.objects.all().order_by("-time_created")
        calculate_2_day = timezone.now() - timedelta(days=2)
        calculate_movie_object = movie_models.Movie.objects.all().filter(
            time_created__gte=calculate_2_day)
        calculate_serie_object = serie_models.Series.objects.all().filter(
            time_created__gte=calculate_2_day
        )
        calculate_movie_object_ids = calculate_movie_object.values_list(
            "id", flat=True)
        calculate_serie_object_ids = calculate_serie_object.values_list(
            "id", flat=True)
        new_movies = {
            movie.id: True if movie.id in calculate_movie_object_ids else False for movie in all_movies}
        new_series = {
            serie.id: True if serie.id in calculate_serie_object_ids else False for serie in all_series}
        return new_movies, new_series

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = entry_models.Category.objects.all()
        search = self.search()
        if settings.DEBUG:
            new_movies, new_series = self.get_new_added_films()
        else:
            new_movies, new_series = self.get_new_added_films_from_cache()
        paginator = Paginator(search, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        for obj in results.object_list:
            if isinstance(obj, movie_models.Movie):
                obj.is_new = new_movies.get(obj.id, False)
            elif isinstance(obj, serie_models.Series):
                obj.is_new = new_series.get(obj.id, False)

        context['results'] = results
        context['new_movies'] = new_movies
        context['new_series'] = new_series
        return context

    @staticmethod
    def get_new_added_films_from_cache():
        """
        add newly added movies to cache
        """
        added_new_films_keys = "added_new_films_keys"
        get_newly_added_films_from_cache = cache.get(added_new_films_keys)
        if not get_newly_added_films_from_cache:
            get_newly_added_films_from_cache = SearchPage.get_new_added_films()
            cache.set(added_new_films_keys, get_newly_added_films_from_cache)
        return get_newly_added_films_from_cache


search_page = SearchPage.as_view()
