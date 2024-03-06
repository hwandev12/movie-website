from django.shortcuts import render
from django.views import generic
from . import models

class HomePageView(generic.ListView):
    model = models.Category
    context_object_name = "categories"
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
# make classes as views name
home_page_view = HomePageView.as_view()