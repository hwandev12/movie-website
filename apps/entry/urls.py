from django.urls import path
from . import views

app_name="entry"

urlpatterns = [
    path("", views.home_page_view, name="home")
]