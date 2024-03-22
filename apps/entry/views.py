from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache


from . import models
from apps.movie import models as movie_models
from apps.series import models as series_models

import random
import json


class HomePageView(generic.ListView):
    model = models.Category
    context_object_name = "categories"
    template_name = "home.html"

    @staticmethod
    def get_latest_movies():
        """
        Get the latest 10 movies.
        """
        two_days_filter_get_variable = timezone.now() - timedelta(days=2)
        new_movies_uploaded = movie_models.Movie.objects.all().filter(
            time_created__gte=two_days_filter_get_variable)
        if new_movies_uploaded.exists():
            new_movie_ids = new_movies_uploaded.values_list("id", flat=True)
            latest_movies = movie_models.Movie.objects.exclude(
                id__in=new_movie_ids).order_by("-time_created")[:10]
        else:
            latest_movies = movie_models.Movie.objects.all().order_by(
                "-time_created")[:10]

        return latest_movies, new_movies_uploaded

    @staticmethod
    def get_latest_series():
        """
        Get the latest 10 series.
        """
        two_days_filter_get_variable = timezone.now() - timedelta(days=2)
        new_series_uploaded = series_models.Series.objects.filter(
            time_created__gte=two_days_filter_get_variable)
        if new_series_uploaded.exists():
            new_series_ids = new_series_uploaded.values_list("id", flat=True)
            new_series = series_models.Series.objects.exclude(
                id__in=new_series_ids).order_by("-time_created")[:10]
        else:
            new_series = series_models.Series.objects.all().order_by(
                "-time_created")[:10]
        return new_series, new_series_uploaded

    @staticmethod
    def get_shows_for_main():
        """
        Get latest movies and series marked as main.
        """
        latest_movies = list(movie_models.Movie.objects.filter(
            main=True).order_by("-time_created"))
        latest_series = list(series_models.Series.objects.filter(
            main=True).order_by("-time_created"))

        latest_content = [{'content': movie, 'type': 'movie'}
                          for movie in latest_movies]
        latest_content.extend(
            [{'content': series, 'type': 'series'} for series in latest_series])

        # Sort the combined list by time_created
        latest_content.sort(
            key=lambda x: x['content'].time_created, reverse=True)

        return latest_content

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_movies'] = self.get_latest_movies_cached()[0]
        context['latest_movies_2_days'] = self.get_latest_movies_cached()[1]
        context['latest_series'] = self.get_latest_series_cached()[0]
        context['latest_series_2_days'] = self.get_latest_series_cached()[1]
        context['latest_shows'] = self.get_shows_for_main_cached()
        context['DEBUG'] = settings.DEBUG
        return context

    @staticmethod
    def get_latest_movies_cached():
        """
        Get the latest 10 movies with caching.
        """
        cache_key = "latest_movies-key"
        latest_movies = cache.get(cache_key)
        if not latest_movies:
            latest_movies = HomePageView.get_latest_movies()
            cache.set(cache_key, latest_movies, timeout=24*60*60)
        return latest_movies

    @staticmethod
    def get_latest_series_cached():
        """
        Get the latest 10 series with caching.
        """
        cache_key = "latest_series-key"
        latest_series = cache.get(cache_key)
        if not latest_series:
            latest_series = HomePageView.get_latest_series()
            cache.set(cache_key, latest_series, timeout=24*60*60)
        return latest_series

    @staticmethod
    def get_shows_for_main_cached():
        """
        Get latest movies and series marked as main with caching.
        """
        cache_key = "get_shows-key"
        get_shows_form_main_variable = cache.get(cache_key)
        if not get_shows_form_main_variable:
            get_shows_form_main_variable = HomePageView.get_shows_for_main()
            cache.set(cache_key, get_shows_form_main_variable,
                      timeout=24*60*60)
        return get_shows_form_main_variable

    @staticmethod
    def invalidate_cache():
        """
        method to invalidate cache when post or something happend
        could be called in everywhere
        """
        cache.delete_many(
            ['latest_movies-key', 'latest_series-key', 'get_shows-key'])


# make classes as views name
home_page_view = HomePageView.as_view()
