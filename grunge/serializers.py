import pdb

from furl import furl
from rest_framework import serializers
from rest_framework.reverse import reverse as drf_reverse

from .fields import UUIDHyperlinkedIdentityField
from .models import Album, Artist, Track, TrackAndOrder, Playlist


class TrackAlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name")


class TrackAlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="album-detail")
    artist = TrackAlbumArtistSerializer()

    class Meta:
        model = Album
        fields = ("uuid", "url", "name", "artist")


class TrackSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="track-detail")
    album = TrackAlbumSerializer()

    class Meta:
        model = Track
        fields = ("uuid", "url", "name", "number", "album")


class AlbumTrackSerializer(TrackSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="track-detail")

    class Meta:
        model = Track
        fields = ("uuid", "url", "name", "number")


class AlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name")


class AlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="album-detail")
    artist = AlbumArtistSerializer()
    tracks = AlbumTrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ("uuid", "url", "name", "year", "artist", "tracks")


class ArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")
    albums_url = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name", "albums_url")

    def get_albums_url(self, artist):
        path = drf_reverse("album-list", request=self.context["request"])
        return furl(path).set({"artist_uuid": artist.uuid}).url


class PlaylistNameSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()

    class Meta:
        model = Playlist
        fields = "__all__"


class TrackAndOrderSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    order = serializers.ReadOnlyField()
    track_name = serializers.ReadOnlyField(source="track.name")
    track_id = serializers.ReadOnlyField(source="track.id")
    playlist_name = serializers.ReadOnlyField(source="playlist.name")
    playlist_id = serializers.ReadOnlyField(source="playlist.id")
    playlist_track_details = UUIDHyperlinkedIdentityField(view_name="playlisttrack-detail")

    class Meta:
        model = TrackAndOrder
        read_only_fields = ("uuid", "order", "track_name", "playlist_name")
        fields = ("uuid", "track", "playlist", "order", "track_name", "playlist_name", "playlist_id", "track_id", "playlist_track_details")

    def save(self, **kwargs):
        if TrackAndOrder.objects.filter(playlist=self.validated_data['playlist'],
                                        track=self.validated_data['track']).exists():
            return TrackAndOrder.objects.filter(playlist=self.validated_data['playlist'],
                                                track=self.validated_data['track'])
        order = TrackAndOrder.objects.filter(playlist=self.validated_data['playlist']).count() + 1

        return TrackAndOrder.objects.create(playlist=self.validated_data['playlist'],
                                            track=self.validated_data['track'], order=order)
