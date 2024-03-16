from django.urls import path
from . import views

app_name = "serie"

urlpatterns = [
    path("single-movie/<int:serieID>/", views.serie_detail_view, name="serie_detail")
]