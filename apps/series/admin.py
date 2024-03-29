from django.contrib import admin
from . import models
from apps.entry.views import HomePageView


class SeriesTrailerInline(admin.TabularInline):
    model = models.SeriesTrailer
    fieldsets = (
        ("", {
            "fields": ("title", "url")
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'title':
            field.label = "Trailer Nomi"
        if db_field.name == "url":
            field.label = "manzil"
        return field


class SeriesModelAdmin(admin.ModelAdmin):
    inlines = (SeriesTrailerInline, )
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        HomePageView.invalidate_cache()
        
class EpisodeModelAdmin(admin.ModelAdmin):
    fieldsets = (
        ("", {
            "fields": ("title", "description", "release_date", "duration_time", "series", "season_number", "episode_number", "card")
        }),
    )



admin.site.register(models.Series, SeriesModelAdmin)
admin.site.register(models.Episode, EpisodeModelAdmin)
