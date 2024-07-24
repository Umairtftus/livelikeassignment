from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve


from .views import PlaylistListView, PlaylistDetailView, PlaylistCreateView, PlaylistUpdateView, PlaylistDeleteView, \
    PlaylistAddTracksView, ChangeOrder
from .viewsets import AlbumViewSet, ArtistViewSet, TrackViewSet, PlaylistNameViewSet, PlaylistViewSet

urlpatterns = []


if settings.DJANGO_ADMIN_ENABLED:
    urlpatterns += [
        re_path("^$", RedirectView.as_view(url="/dashboard/", permanent=True)),
        path("dashboard", PlaylistListView.as_view(), name="dashboard"),
        path("playlists/", PlaylistListView.as_view(), name="playlist_list"),
        path("playlists/<int:pk>/", PlaylistDetailView.as_view(), name="playlist_detail"),
        path("playlists/create/", PlaylistCreateView.as_view(), name="playlist_create"),
        path("playlists/<int:pk>/add-tracks/", PlaylistAddTracksView.as_view(), name="playlist_add_tracks"),
        path("playlists/<int:pk>/update/", PlaylistUpdateView.as_view(), name="playlist_update"),
        path("playlists/<int:pk>/delete/", PlaylistDeleteView.as_view(), name="playlist_delete"),
        path("playlists/<int:pk>/change-order/", ChangeOrder.as_view(), name="change_track_order"),
        path("admin/", admin.site.urls),
    ]


if settings.DJANGO_API_ENABLED:
    api_router = DefaultRouter(trailing_slash=False)
    api_router.register("artists", ArtistViewSet)
    api_router.register("albums", AlbumViewSet)
    api_router.register("tracks", TrackViewSet)
    api_router.register("playlists", PlaylistNameViewSet, basename="_playlist")
    api_router.register("playlisttrack", PlaylistViewSet, basename='playlisttrack')

    urlpatterns += [
        path("api/<version>/", include(api_router.urls)),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns.append(
        re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT})
    )