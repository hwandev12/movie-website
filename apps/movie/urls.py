from django.urls import path
from . import views

app_name='movie'

urlpatterns = [
    path("single/<int:movieID>/", views.movie_single, name='single')
]