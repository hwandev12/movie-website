from typing import Any
from django.contrib import admin
from django.db.models.fields import Field
from django.http import HttpRequest
from . import models
from apps.entry.views import HomePageView

class TrailerInline(admin.TabularInline):
    model = models.Trailer
    fieldsets = (
        ("",{
            'fields': ("title", "url")  
        }),
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'title':
            field.label = "Trailer uchun nom"
        if db_field.name == "url":
            field.label = "Trailer Manzil(Youtube link)"
        return field

class CustomMovieModelAdmin(admin.ModelAdmin):
    inlines = (TrailerInline, )
    prepopulated_fields = {"slug": ('title',)}
    # Define fields you want to customize
    fieldsets = (
        ('', {
            'fields': ('title', 'description', 'release_date', 'director', 'actors', 'genre', 'countries', 'duration_time', 'rating', 'quality', 'main', 'is_movie', 'poster', 'card_poster', 'video_url', 'slug')
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'title':
            field.label = 'Kino nomi'
        if db_field.name == 'description':
            field.label = "Kino Haqida"
        if db_field.name == "release_date":
            field.label = "Chiqqan Sana"
        if db_field.name == "genre":
            field.label = "Janr"
        if db_field.name == "countries":
            field.label = "Davlati"
        if db_field.name == "duration_time":
            field.label = "Kino vaqti"
        if db_field.name == "rating":
            field.label = "Reyting"
        if db_field.name == "quality":
            field.label = "Sifati"
        if db_field.name == "poster":
            field.label = "Katta banner uchun rasm"
        if db_field.name == "card_poster":
            field.label = "Kichik kino card uchun rasm"
        if db_field.name == "main":
            field.label = "Asosiy qilinsinmi?"
        if db_field.name == 'is_movie':
            field.label = 'Kino'
        if db_field.name == "video_url":
            field.label = "Video Manzil"
        return field
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        HomePageView.invalidate_cache()


MODELS = (
    models.GenreChoices,
    models.QualityChoices,
)

[admin.site.register(model) for model in MODELS]
admin.site.register(models.Movie, CustomMovieModelAdmin)
