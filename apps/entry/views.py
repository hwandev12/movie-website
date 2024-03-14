from django.shortcuts import render
from django.views import generic
from . import models
from apps.movie import models as movie_models
from apps.series import models as series_models

import random

class HomePageView(generic.ListView):
    model = models.Category
    context_object_name = "categories"
    template_name = "home.html"
    
    def get_movies_for_main(self):
        """
        Barcha asosiy deb belgilagan kinolarmni olish uchun
        """
        movies = movie_models.Movie.objects.all().filter(main=True).order_by("-time_created")[1:]
        return movies
    
    def get_series_for_main(self):
        """
        Barcha asosiy deb belgilagan kinolarni olish uchun
        """
        series = series_models.Series.objects.all().filter(main=True).order_by("-time_created")
        return series
    
    def get_first_movie_main(self):
        movie = movie_models.Movie.objects.filter(main=True).order_by("-time_created").first()
        return movie
    
    def get_latest_movies(self):
        """
        Eng oxirgi qo'shilgan 10ta kinoni olib beradi
        """
        movies = movie_models.Movie.objects.all().order_by("-time_created")[:10]
        return movies
    
    def get_latest_series(self):
        """
        eng oxirgi qo'shilgan serialarni olish
        """
        series = series_models.Series.objects.all().order_by("-time_created")[:10]
        return series
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = self.get_movies_for_main()
        context['series'] = self.get_series_for_main()
        context['movie'] = self.get_first_movie_main()
        context['latest_movies'] = self.get_latest_movies()
        context['latest_series'] = self.get_latest_series()
        return context
    
    
# make classes as views name
home_page_view = HomePageView.as_view()