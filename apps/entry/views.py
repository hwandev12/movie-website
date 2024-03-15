from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse




from . import models
from apps.movie import models as movie_models
from apps.series import models as series_models

import random
import json
class HomePageView(generic.ListView):
    model = models.Category
    context_object_name = "categories"
    template_name = "home.html"
    
    def get_first_movie_main(self):
        movie = movie_models.Movie.objects.filter(main=True).order_by("-time_created").first()
        serie = series_models.Series.objects.filter(main=True).order_by("-time_created").first()
        
        if movie is not None and serie is not None:
            
            return sorted([movie, serie], key=lambda x: x.time_created, reverse=True)
        elif movie is not None:
            return [movie]
        elif serie is not None:
            return [serie]
        else:
            return []
    
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
    
    def get_shows_for_main(self):
        latest_movies = list(movie_models.Movie.objects.all().filter(main=True).order_by("-time_created")[1:])
        latest_series = list(series_models.Series.objects.all().filter(main=True).order_by("-time_created")[1:])
        
        latest_content = [{'content': movie, 'type': 'movie'} for movie in latest_movies]
        latest_content.extend([{'content': series, 'type': 'series'} for series in latest_series])
        
        # Sort the combined list by time_created
        latest_content.sort(key=lambda x: x['content'].time_created, reverse=True)
        
        return latest_content
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_movie_section = []
        movie_first = self.get_first_movie_main()
        for m in movie_first:
            if m.is_movie:
                is_movie_section.append(True)
            else:
                is_movie_section.append(False)
        context['movie_first'] = zip(self.get_first_movie_main(), is_movie_section)
        context['latest_movies'] = self.get_latest_movies()
        context['latest_series'] = self.get_latest_series()
        context['latest_shows'] = self.get_shows_for_main()
        return context
    
    
# make classes as views name
home_page_view = HomePageView.as_view()