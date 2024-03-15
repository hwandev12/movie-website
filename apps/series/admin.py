from django.contrib import admin
from . import models


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


admin.site.register(models.Series, SeriesModelAdmin)
admin.site.register(models.Episode)
