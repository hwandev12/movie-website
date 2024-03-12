from django.contrib import admin
from . import models


class CustomMovieModelAdmin(admin.ModelAdmin):
    # Define fields you want to customize
    fieldsets = (
        ('', {
            'fields': ('title', 'description', 'release_date', 'director', 'actors', 'genre', 'countries', 'duration_time', 'rating', 'quality', 'poster', 'card_poster')
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
        return field


MODELS = (
    models.GenreChoices,
    models.QualityChoices,
)

[admin.site.register(model) for model in MODELS]
admin.site.register(models.Movie, CustomMovieModelAdmin)
