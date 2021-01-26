from unittest import skip

from . import BaseAPITestCase


class PlaylistTests(BaseAPITestCase):
    def setUp(self):
        pass

    @skip
    def test_list_playlists(self):
        # Should be able to fetch the list of playlists.
        raise NotImplementedError("This test case needs to be implemented.")

    @skip
    def test_search_playlists(self):
        # Should be able to search for playlists by `name`.
        raise NotImplementedError("This test case needs to be implemented.")

    @skip
    def test_get_playlist(self):
        # Should be able to fetch a playlist by its `uuid`.
        raise NotImplementedError("This test case needs to be implemented.")

    @skip
    def test_create_playlist(self):
        # Should be able to create a playlist with 0 or more tracks.
        raise NotImplementedError("This test case needs to be implemented.")

    @skip
    def test_update_playlist(self):
        # Should be able to change a playlist's `name`, and add, remove,
        # or re-order tracks.
        raise NotImplementedError("This test case needs to be implemented.")

    @skip
    def test_delete_playlist(self):
        # Should be able to delete a playlist by `uuid`.
        raise NotImplementedError("This test case needs to be implemented.")
