from django_filters import rest_framework as filters

from .models import Album, Artist, Track, TrackAndOrder, Playlist


class ArtistFilter(filters.FilterSet):

    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Artist
        fields = ("name",)


class AlbumFilter(filters.FilterSet):

    artist_uuid = filters.UUIDFilter("artist__uuid")
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Album
        fields = ("artist_uuid", "name")


class TrackFilter(filters.FilterSet):

    album_uuid = filters.UUIDFilter("album__uuid")
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Track
        fields = ("album_uuid", "name")


class PlaylistNameFilter(filters.FilterSet):

    playlist_uuid = filters.UUIDFilter("playlist__uuid")
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Playlist
        fields = ("playlist_uuid", "name")


class TrackAndOrderFilter(filters.FilterSet):

    track_order_uuid = filters.UUIDFilter("trackandorder__uuid")
    trackuuid = filters.UUIDFilter("track__uuid")
    order = filters.NumberFilter(lookup_expr="contains")

    class Meta:
        model = TrackAndOrder
        fields = ("track_order_uuid","trackuuid", "order")

