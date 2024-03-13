from django.shortcuts import render
from django.views import generic

from . import models
from apps.entry import models as entry_models


class MovieSingle(generic.DetailView):
    model = models.Movie
    template_name = 'movies/single_movie.html'
    context_object_name = 'movie'
    pk_url_kwarg = 'movieID'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = entry_models.Category.objects.all()
        return context
    
# make classes to function names
movie_single = MovieSingle.as_view()

