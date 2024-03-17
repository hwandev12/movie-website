from django.urls import path
from . import views

app_name = "serie"

urlpatterns = [
    path("single-movie/<slug:slug>/", views.serie_detail_view, name="serie_detail"),
    path("single-movie/<str:slug>/<int:episodeID>/", views.episode_watch, name='episode')
]