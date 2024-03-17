from django.urls import path
from . import views

app_name='movie'

urlpatterns = [
    path("single/<slug:slug>/", views.movie_single, name='single'),
    path("ajax-single-movie-get/<int:ID>/", views.get_single_video, name='single_video_ajax')
]