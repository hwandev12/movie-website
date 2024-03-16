from django.db import models
from apps.movie.models import GenreChoices, QualityChoices
from django_countries.fields import CountryField
from django.core.validators import URLValidator


class SeriesTrailer(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(URLValidator(schemes="https"))
    movie = models.OneToOneField(
        "Series", on_delete=models.SET_NULL, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Serial Trailer"
        verbose_name_plural = "Serial Trailers"

    def __str__(self):
        return "%s" % self.title


class Series(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    director = models.CharField(max_length=255)
    actors = models.CharField(max_length=255)
    genre = models.ManyToManyField(GenreChoices)
    countries = CountryField(multiple=True)
    rating = models.FloatField()
    quality = models.ManyToManyField(QualityChoices)
    poster = models.ImageField(
        upload_to='series_posters/', null=True, blank=True)
    card = models.ImageField(
        upload_to='series_cards/', null=True, blank=True
    )
    main = models.BooleanField(default=True, null=True)
    is_movie = models.BooleanField(default=False, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def make_capitalize(self):
        return self.title.capitalize()

    def get_title_for_movie_cards(self):
        return self.title.split(maxsplit=2)[0:2]


class Episode(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    duration_time = models.TimeField()
    series = models.ForeignKey(
        Series, on_delete=models.CASCADE, related_name='episodes')
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    card = models.ImageField(
        upload_to='episodes_cards/', null=True, blank=True
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def get_formatted_duration(self):
        hours = self.duration_time.hour
        minutes = self.duration_time.minute
        return f"{hours}h {minutes}min"

    def __str__(self):
        return f"{self.series.title} - Season {self.season_number}, Episode {self.episode_number}: {self.title}"
