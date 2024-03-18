from django.urls import path
from . import views

app_name='movie'

urlpatterns = [
    path("single/<slug:slug>/", views.movie_single, name='single'),
    path("barcha-tarjima-filmlar/", views.movies_list_view, name='movies_list'),
    path("ajax-single-movie-get/<int:ID>/", views.get_single_video, name='single_video_ajax')
]