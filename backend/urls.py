from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.entry.urls")),
    path("movies/", include("apps.movie.urls")),
    path("series/", include("apps.series.urls")),
    path("search/kinolar-seriallar-qidirish/", include("apps.search.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

# redirect user when 404 throws
handler404 = 'apps.entry.views.not_found_page'