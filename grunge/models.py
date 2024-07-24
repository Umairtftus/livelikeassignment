from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class UUIDManager(models.Manager):
    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class UUIDModel(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid4, unique=True)
    objects = UUIDManager()

    class Meta:
        abstract = True

    def natural_key(self):
        return (self.uuid,)


class Artist(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The artist name"))

    class Meta:
        ordering = ("name",)
        indexes = (models.Index(fields=("name",)),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("admin:grunge_artist_change", kwargs={"object_id": self.pk})


class Album(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The album name"))
    year = models.PositiveSmallIntegerField(
        help_text=_("The year the album was released")
    )
    artist = models.ForeignKey(
        Artist,
        help_text=_("The artist that produced the album"),
        related_name="albums",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("artist", "year", "name")
        indexes = (models.Index(fields=("artist", "year", "name")),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("admin:grunge_album_change", kwargs={"object_id": self.pk})


class Track(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The track name"))
    album = models.ForeignKey(
        Album,
        help_text=_("The album this track appears on"),
        related_name="tracks",
        on_delete=models.CASCADE,
    )
    number = models.PositiveSmallIntegerField(
        help_text=_("The track number on the album")
    )

    class Meta:
        ordering = ("number", "name")
        indexes = (models.Index(fields=("number", "name")),)
        constraints = (
            models.UniqueConstraint(
                fields=("album", "number"), name="unique_album_number"
            ),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("admin:grunge_track_change", kwargs={"object_id": self.pk})


class Playlist(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The playlist name"))

    class Meta:
        ordering = ("name",)
        indexes = (models.Index(fields=("name",)),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("playlist_detail", kwargs={"pk": self.pk})


class TrackAndOrder(UUIDModel):
    track = models.ForeignKey(Track, help_text=_("Track refers to the playlist"),
                              related_name="track",
                              on_delete=models.CASCADE)

    order = models.PositiveIntegerField(help_text=_("The Track number on the playlist"), null=True, blank=True,
                                        editable=True)
    playlist = models.ForeignKey(Playlist, null=True, help_text=_("The playlist of the track"),
                                 related_name="playlist_tracks",
                                 on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("admin:grunge_trackandorder_change", kwargs={"object_id": self.pk})

    class Meta:
        ordering = ("order",)
        indexes = (models.Index(fields=("order", "playlist", "track")),)
        constraints = (models.UniqueConstraint(
            fields=("playlist", "track"), name="unique_track"),)

    def __str__(self):
        return self.playlist.name + "-" + self.track.name

    @property
    def name(self):
        return self.track.name
