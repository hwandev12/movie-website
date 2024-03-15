from django.db import models
from django_countries.fields import CountryField
from django.core.validators import URLValidator


class QualityChoices(models.Model):

    name = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Quality Choice"
        verbose_name_plural = "Quality Choices"

    def __str__(self):
        return "%s format" % self.name


class GenreChoices(models.Model):
    name = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    # time_created agar kerak bo'lsa `holatiga`

    class Meta:
        verbose_name = "Genre Choice"
        verbose_name_plural = "Genre Choices"

    def __str__(self):
        return "`%s` -- janr" % self.name

    def get_formatted_title(self):
        words = self.name.split()  # Split the title into words
        # Join words with comma, except for the last one
        formatted_title = ", ".join(words[:-1])
        if words:
            # Add the last word without a comma
            formatted_title += " " + words[-1]
        return formatted_title

class Trailer(models.Model):
    
    title = models.CharField(max_length=100)
    url = models.URLField(URLValidator(schemes="https"))
    movie = models.OneToOneField("Movie", on_delete=models.SET_NULL, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Kino Trailer"
        verbose_name_plural = "Kino Trailers"
    
    def __str__(self):
        return "%s" % self.title

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    director = models.CharField(max_length=255)
    actors = models.CharField(max_length=255)
    genre = models.ManyToManyField(GenreChoices)
    countries = CountryField(multiple=True)
    duration_time = models.TimeField()
    rating = models.FloatField()
    quality = models.ManyToManyField(QualityChoices)
    poster = models.ImageField(
        upload_to='movie_posters/', null=True, blank=True)
    card_poster = models.ImageField(
        upload_to="card_poster/", null=True, blank=True)
    main = models.BooleanField(default=True, null=True)
    is_movie = models.BooleanField(default=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s -- %s" % (self.title, self.release_date)

    def get_formatted_duration(self):
        hours = self.duration_time.hour
        minutes = self.duration_time.minute
        return f"{hours}h {minutes}min"

    def make_capitalize(self):
        return self.title.capitalize()

    def get_title_for_movie_cards(self):
        return self.title.split(maxsplit=2)[0:2]
