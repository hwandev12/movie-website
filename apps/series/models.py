from django.db import models
from apps.movie.models import GenreChoices, QualityChoices
from django_countries.fields import CountryField


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
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.series.title} - Season {self.season_number}, Episode {self.episode_number}: {self.title}"
