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
        movies = movie_models.Movie.objects.all()
        return movies
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = self.get_movies()
        return context
    
    
# make classes as views name
home_page_view = HomePageView.as_view()