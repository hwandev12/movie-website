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
            "fields": ("title", "description", "release_date", "duration_time", "series", "season_number", 'video_url', "episode_number", "card")
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'title':
            field.label = "Qism nomi"
        if db_field.name == "video_url":
            field.label = "Video Manzil"
        if db_field.name == "description":
            field.label = "Qism haqida"
        if db_field.name == "release_date":
            field.label = "Qism Chiqish sanasi"
        if db_field.name == "duration_time":
            field.label = "Qism vaqti"
        if db_field.name == "series":
            field.label = "Seriya"
        if db_field.name == "season_number":
            field.label = "Nechanchi fasl"
        if db_field.name == "episode_number":
            field.label = "Nechanchi qism"
        return field


admin.site.register(models.Series, SeriesModelAdmin)
admin.site.register(models.Episode, EpisodeModelAdmin)
