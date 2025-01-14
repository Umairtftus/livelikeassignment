import pdb
from unittest import skip
from uuid import UUID

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
        self.playlist_uuid = UUID("9e52205f-9927-4eff-b132-ce10c6f3e0b1")
        self.playlist = Playlist.objects.create(name="My Playlist", uuid=self.playlist_uuid)
        self.artist = Artist.objects.create(name="Artist")
        self.album = Album.objects.create(name="Album 1", year=2019, artist=self.artist)
        self.track1 = Track.objects.create(name="Track 1", number=1, album=self.album)
        self.track2 = Track.objects.create(name="Track 2", number=2, album=self.album)
        self.track3 = Track.objects.create(name="Track 3", number=3, album=self.album)
        self.track_order1 = TrackAndOrder.objects.create(track=self.track1, playlist=self.playlist, order=1)
        self.track_order2 = TrackAndOrder.objects.create(track=self.track2, playlist=self.playlist, order=2)
        self.track_order3 = TrackAndOrder.objects.create(track=self.track3, playlist=self.playlist, order=3)
        self.playlist_url = reverse('_playlist-list', kwargs={'version': 'v1'})  # Correct URL name

    def test_list_playlists(self):
        response = self.client.get(self.playlist_url)
        playlists = Playlist.objects.all()
        serializer = PlaylistNameSerializer(playlists, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_playlist(self):
        response = self.client.get(reverse('_playlist-detail', kwargs={'version': 'v1', 'uuid': self.playlist_uuid}))
        playlist = Playlist.objects.get(uuid=self.playlist.uuid)
        serializer = PlaylistNameSerializer(playlist)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_playlist(self):
        data = {'name': 'New Playlist'}
        response = self.client.post(self.playlist_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], 'Playlist added successfully!')

    def test_update_playlist(self):
        data = {'name': 'Updated Playlist'}
        response = self.client.put(reverse('_playlist-detail', kwargs={'version': 'v1','uuid': self.playlist_uuid}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.name, 'Updated Playlist')

    def test_delete_playlist(self):
        response = self.client.delete(reverse('_playlist-detail', kwargs={'version': 'v1','uuid': self.playlist_uuid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], 'Deleted Successfully!')
        with self.assertRaises(Playlist.DoesNotExist):
            Playlist.objects.get(uuid=self.playlist.uuid)

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
