import pdb

from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from .filters import AlbumFilter, ArtistFilter, TrackFilter, TrackAndOrderFilter, PlaylistNameFilter
from .models import Album, Artist, Track, TrackAndOrder, Playlist
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer, PlaylistNameSerializer, \
    TrackAndOrderSerializer


class BaseAPIViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class ArtistViewSet(BaseAPIViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_class = ArtistFilter


class AlbumViewSet(BaseAPIViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_class = AlbumFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("artist").prefetch_related("tracks")


class TrackViewSet(BaseAPIViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_class = TrackFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("album", "album__artist")


class PlaylistNameViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    queryset = Playlist.objects.all()
    serializer_class = PlaylistNameSerializer
    filter_class = PlaylistNameFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related()

    def list(self, request, version=None):
        serialized_data = self.serializer_class(self.queryset, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Playlist added successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, version, uuid=None):
        playlist = get_object_or_404(self.queryset, uuid=uuid)
        serialized_data = self.serializer_class(playlist)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def destroy(self, request, version, uuid=None):
        playlist = get_object_or_404(self.queryset, uuid=uuid)
        if playlist:
            playlist.delete()
            return Response({"msg": "Deleted Successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Unable to delete!"}, status=status.HTTP_200_OK)


class PlaylistViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    queryset = TrackAndOrder.objects.all()
    serializer_class = TrackAndOrderSerializer
    filter_class = TrackAndOrderFilter

    def destroy(self, request, version, uuid=None):
        playlist = get_object_or_404(self.queryset, uuid=uuid)

        if playlist:
            playlist.delete()
            TrackAndOrder.object.filter(playlist=playlist.playlist, order__gte=playlist.order).update(order=F('order') - 1)
            return Response({"msg": "Deleted Successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Unable to delete!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'],
            url_path='reorder1/(?P<track_id>[^/.]+)/(?P<playlist_id>[^/.]+)/(?P<position>[^/.]+)')
    def reorder(self, request, version, track_id, playlist_id, position, *args, **kwargs):
        position = int(position)
        playlist_tracks = TrackAndOrder.objects.filter(playlist_id=playlist_id)
        position = min(position, playlist_tracks.count())
        current_track = playlist_tracks.get(track_id=track_id)
        current_order = current_track.order

        if current_order < position:
            # Moving the track down
            for track in playlist_tracks:
                if current_order < track.order <= position:
                    track.order -= 1
                    track.save()
        elif current_order > position:
            # Moving the track up
            for track in playlist_tracks:
                if position <= track.order < current_order:
                    track.order += 1
                    track.save()

        current_track.order = position

        current_track.save()

        return Response({"msg": "Successfully reordered!"})
