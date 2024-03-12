from django.shortcuts import render
from django.views import generic
from . import models
from apps.movie import models as movie_models

import random

class HomePageView(generic.ListView):
    model = models.Category
    context_object_name = "categories"
    template_name = "home.html"
    
    def get_movies(self):
        """
        Barcha asosiy deb belgilagan kinolarmni olish uchun
        """
        movies = movie_models.Movie.objects.all().filter(main=True).order_by("-time_created")[1:]
        return movies
    
    def get_first_movie_main(self):
        movie = movie_models.Movie.objects.filter(main=True).order_by("-time_created").first()
        return movie
    
    def get_latest_movies(self):
        """
        Eng oxirgi qo'shilgan 10ta kinoni olib beradi
        """
        movies = movie_models.Movie.objects.all().order_by("-time_created")[:10]
        return movies
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = self.get_movies()
        context['movie'] = self.get_first_movie_main()
        context['latest_movies'] = self.get_latest_movies()
        return context
    
    
# make classes as views name
home_page_view = HomePageView.as_view()