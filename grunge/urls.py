from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from .views import PlaylistListView, PlaylistDetailView, PlaylistCreateView, PlaylistUpdateView, PlaylistDeleteView
from .viewsets import AlbumViewSet, ArtistViewSet, TrackViewSet, PlaylistNameViewSet, PlaylistViewSet

urlpatterns = []


# if settings.DJANGO_ADMIN_ENABLED:
#     urlpatterns += [
#         re_path("^$", RedirectView.as_view(url="/admin/", permanent=True)),
#         path("playlists/", PlaylistListView.as_view(), name="playlist_list"),
#         path("playlists/<uuid:pk>/", PlaylistDetailView.as_view(), name="playlist_detail"),
#         path("playlists/create/", PlaylistCreateView.as_view(), name="playlist_create"),
#         path("playlists/<uuid:pk>/update/", PlaylistUpdateView.as_view(), name="playlist_update"),
#         path("playlists/<uuid:pk>/delete/", PlaylistDeleteView.as_view(), name="playlist_delete"),
#         path("admin/", admin.site.urls),
#     ]


if settings.DJANGO_API_ENABLED:
    api_router = DefaultRouter(trailing_slash=False)
    api_router.register("artists", ArtistViewSet)
    api_router.register("albums", AlbumViewSet)
    api_router.register("tracks", TrackViewSet)
    api_router.register("playlist1", PlaylistNameViewSet, basename="_playlist")
    api_router.register("playlisttrack", PlaylistViewSet, basename='playlisttrack')

    urlpatterns += [
        path("api/<version>/", include(api_router.urls)),
    ]