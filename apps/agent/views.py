from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from botocore.client import Config
from boto3.s3.transfer import TransferConfig
from retrying import retry
from django.contrib import messages

from apps.movie import models as movie_models
from apps.series import models as serie_models

import boto3
import botocore
import sys
import os


class AgentMoviePage(generic.ListView):
    model = movie_models.Movie
    context_object_name = 'movies'
    template_name = "agent/movies.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-time_created")


class AgentSeriePage(generic.ListView):
    model = serie_models.Series
    context_object_name = 'series'
    template_name = "agent/series.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-time_created")
    
class SerieEpisodesViewPage(generic.ListView):
    model = serie_models.Episode
    context_object_name = 'episodes'
    template_name = 'agent/episodes.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(series__id=self.kwargs.get("serie_id"))
    
class EpisodeDetailView(generic.DetailView):
    model = serie_models.Episode
    context_object_name = 'episode'
    template_name = 'agent/episode_detail.html'
    pk_url_kwarg = 'episode_id'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-time_created")
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if 'video_serie' in request.FILES:
            return self.handle_chunk_upload(request)
        else:
            return JsonResponse({"error": "No chunk is provided"}, status=400)
        
    def handle_chunk_upload(self, request):
        episode_id = self.kwargs.get("episode_id", "")
        episode = get_object_or_404(serie_models.Episode, pk=episode_id)
        
        chunk = request.FILES.get("video_serie")
        
        s3_client = boto3.client('s3', endpoint_url='https://nyc3.digitaloceanspaces.com',
                                 aws_access_key_id="DO00NVDU8AVAP3PXX4BM",
                                 aws_secret_access_key="QwdwTqCO6ONmcw97ST3Qi/SZj54ECv1sIbh5Eqt4DOk")

        config = TransferConfig(multipart_threshold=1024*20,
                                max_concurrency=3,
                                multipart_chunksize=1024*20,
                                use_threads=True)
        filename = os.path.basename(chunk.name)
        s3_key = f"files/media/series/videos/{filename}"
        with chunk.open('rb') as data:
            s3_client.upload_fileobj(
                Fileobj=data,
                Bucket="movie-django",
                Key=s3_key,
                Config=config
            )
        trimmed_s3_key = s3_key.split('files/media/')[1]
        episode.video = trimmed_s3_key
        episode.save()
        messages.success(self.request, "Siz muvaffaqiyatli film yukladingiz")
        url_to_redirect = reverse("agent:episodes", args=[episode.series.id])
        return redirect(url_to_redirect)

class MovieDetailPage(generic.DetailView):
    model = movie_models.Movie
    context_object_name = 'movie'
    template_name = 'agent/movie_detail.html'

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if 'video' in request.FILES:
            return self.handle_chunk_upload(request)
        else:
            return JsonResponse({'error': 'No chunk provided'}, status=400)

    def handle_chunk_upload(self, request):
        movie_id = self.kwargs.get("pk", "")
        movie = get_object_or_404(movie_models.Movie, pk=movie_id)

        chunk = request.FILES.get("video")

        s3_client = boto3.client('s3', endpoint_url='https://nyc3.digitaloceanspaces.com',
                                 aws_access_key_id="DO00NVDU8AVAP3PXX4BM",
                                 aws_secret_access_key="QwdwTqCO6ONmcw97ST3Qi/SZj54ECv1sIbh5Eqt4DOk")

        config = TransferConfig(multipart_threshold=1024*20,
                                max_concurrency=3,
                                multipart_chunksize=1024*20,
                                use_threads=True)
        filename = os.path.basename(chunk.name)
        s3_key = f"files/media/movies/videos/{filename}"
        with chunk.open('rb') as data:
            s3_client.upload_fileobj(
                Fileobj=data,
                Bucket="movie-django",
                Key=s3_key,
                Config=config
            )
        trimmed_s3_key = s3_key.split('files/media/')[1]
        movie.video = trimmed_s3_key
        movie.save()
        messages.success(self.request, "Siz muvaffaqiyatli film yukladingiz")
        url_to_redirect = reverse("agent:movie_detail", args=[movie_id])
        return redirect(url_to_redirect)

# class EpisodeVideoUploadPage(generic.DetailView):


agent_movie_page = AgentMoviePage.as_view()
agent_serie_page = AgentSeriePage.as_view()
agent_movie_detail_page = MovieDetailPage.as_view()

episodes_of_series_page = SerieEpisodesViewPage.as_view()
episode_detail_page = EpisodeDetailView.as_view()