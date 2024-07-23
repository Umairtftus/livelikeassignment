from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from .filters import AlbumFilter, ArtistFilter, TrackFilter, TrackAndOrderFilter, PlaylistNameFilter
from .models import Album, Artist, Track, TrackAndOrder, Playlist
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer, PlaylistNameSerializer, TrackAndOrderSerializer


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
    queryset = Playlist.objects.all()
    serializer_class = PlaylistNameSerializer
    filter_class = PlaylistNameFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related()

    def list(self, request, version=None):
        serialized_data = self.serializer_class(self.queryset, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def create(self, request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Playlist added successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Unable to add playlist !!"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, version, pk=None):
        playlist = get_object_or_404(self.queryset, pk=pk)
        serialized_data = self.serializer_class(playlist)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def destroy(self, request, version, pk=None):
        playlist = get_object_or_404(self.queryset, pk=pk)
        if playlist:
            playlist.delete()
            return Response({"msg": "Deleted Successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Unable to delete!"}, status=status.HTTP_200_OK)


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = TrackAndOrder.objects.all()
    serializer_class = TrackAndOrderSerializer
    filter_class = TrackAndOrderFilter

    def list(self, request,version):
        serialized_data = self.serializer_class(self.queryset, many=True)
        return Response(serialized_data.data,status=status.HTTP_200_OK)

    def create(self, request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Track added successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Unable to add track !!"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, version, pk=None ):
        playlist = get_object_or_404(self.queryset, pk=pk)
        serialized_data = self.serializer_class(playlist)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def destroy(self, request, version, pk=None):
        playlist = get_object_or_404(self.queryset, pk=pk)
        if playlist:
            playlist.delete()
            return Response({"msg": "Deleted Successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Unable to delete!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], name='Reorder Track', url_path="reorder1/<str:trackid>/<str:position>/")
    def reorder(self, request,version,trackid,position, *args,**kwargs):
        return Response({"msg":"Successfully fetched!"})




