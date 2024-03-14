"""
URL configuration for movie_site project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from movie_site import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("movies.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
