from django.db import models
from django_countries.fields import CountryField

class GenreChoices(models.Model):
    name = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    # time_created agar kerak bo'lsa `holatiga`
    
    def __str__(self):
        return "`%s` -- janr" % self.name

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
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)

    def __str__(self):
        return self.title
