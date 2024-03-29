from django.urls import path
from . import views

app_name = 'agent'

urlpatterns = [
    path("", views.agent_movie_page, name='agent_movie'),
    path("series/", views.agent_serie_page, name='agent_serie'),
    path("movie/<int:pk>/", views.agent_movie_detail_page, name='movie_detail'),
    # episodes
    path("episodes/<int:serie_id>/", views.episodes_of_series_page, name='episodes'),
    path("serie/episode/detail/<int:episode_id>/", views.episode_detail_page, name='episode_detail'),
]