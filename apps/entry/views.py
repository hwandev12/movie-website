from django.shortcuts import render
from django.views import generic

class HomePageView(generic.TemplateView):
    template_name = "home.html"
    
    
# make classes as views name
home_page_view = HomePageView.as_view()