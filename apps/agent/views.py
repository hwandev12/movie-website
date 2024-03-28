from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.base import ContentFile

from apps.movie import models as movie_models
from apps.series import models as serie_models


class AgentMoviePage(generic.ListView):
    model = movie_models.Movie
    context_object_name = 'movies'
    template_name = "agent/movies.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-time_created")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect("/")
        return super().dispatch(*args, **kwargs)


class AgentSeriePage(generic.ListView):
    model = serie_models.Series
    context_object_name = 'series'
    template_name = "agent/series.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-time_created")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect("/")
        return super().dispatch(*args, **kwargs)


class MovieDetailPage(generic.DetailView):
    model = movie_models.Movie
    context_object_name = 'movie'
    template_name = 'agent/movie_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect("/")
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'chunk' in self.request.FILES:
            return self.handle_chunk_upload(request)
        else:
            return JsonResponse({'error': 'No chunk provided'}, status=400)
        
    def handle_chunk_upload(self, request):
        movie_id = self.kwargs.get("pk", "")
        movie = get_object_or_404(movie_models.Movie, pk=movie_id)

        chunk = self.request.FILES['chunk']

        movie.video.save(chunk.name, chunk, save=True)

        return JsonResponse({"success": "Uploaded successfully"})

# class EpisodeVideoUploadPage(generic.DetailView):
    


agent_movie_page = AgentMoviePage.as_view()
agent_serie_page = AgentSeriePage.as_view()
agent_movie_detail_page = MovieDetailPage.as_view()
