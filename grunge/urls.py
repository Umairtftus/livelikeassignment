from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import AlbumViewSet, ArtistViewSet, TrackViewSet

urlpatterns = []


class APIRouter(DefaultRouter):
    pass


if settings.DJANGO_ADMIN_ENABLED:
    urlpatterns += [path("admin/", admin.site.urls)]

if settings.DJANGO_API_ENABLED:
    api_router = APIRouter(trailing_slash=False)
    api_router.register("artists", ArtistViewSet)
    api_router.register("albums", AlbumViewSet)
    api_router.register("tracks", TrackViewSet)

    urlpatterns += [
        path("api/<version>/", include(api_router.urls)),
    ]
