from unittest import skip
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from . import BaseAPITestCase
from ..models import Playlist, Track, TrackAndOrder, Artist, Album
from ..serializers import PlaylistNameSerializer


from unittest import skip
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from . import BaseAPITestCase
from ..models import Playlist, Track, TrackAndOrder, Artist, Album
from ..serializers import PlaylistNameSerializer

class PlaylistTests(BaseAPITestCase):
    def setUp(self):
        self.playlist = Playlist.objects.create(name="My Playlist")
        self.artist = Artist.objects.create(name="Artist")
        self.album = Album.objects.create(name="Album 1", year=2019, artist=self.artist)
        self.track1 = Track.objects.create(name="Track 1", number=1, album=self.album)
        self.track2 = Track.objects.create(name="Track 2", number=2, album=self.album)
        self.track3 = Track.objects.create(name="Track 3", number=3, album=self.album)
        self.track_order1 = TrackAndOrder.objects.create(track=self.track1, playlist=self.playlist, order=1)
        self.track_order2 = TrackAndOrder.objects.create(track=self.track2, playlist=self.playlist, order=2)
        self.track_order3 = TrackAndOrder.objects.create(track=self.track3, playlist=self.playlist, order=3)
        self.playlist_url = reverse('playlisttrack-list', kwargs={'version': 'v1'})

    def test_reorder_playlist_tracks(self):
        response = self.client.patch(
            reverse('playlisttrack-reorder', kwargs={
                'version': 'v1',
                'track_id': self.track1.pk,
                'playlist_id': self.playlist.pk,
                'position': 2
            })
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], 'Successfully reordered!')
        self.track_order1.refresh_from_db()
        self.assertEqual(self.track_order1.order, 2)

    def test_reorder_tracks_on_delete(self):
        response = self.client.delete(
            reverse('playlisttrack-destroy', kwargs={
                'version': 'v1',
                'pk': self.track2.pk,
            })
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], 'Successfully reordered!')
        self.track_order3.refresh_from_db()
        self.assertEqual(self.track_order3.order, 2)
