# forms.py
import pdb

from django import forms
from django.forms import inlineformset_factory
from django.db.models import Max
from .models import Playlist, TrackAndOrder


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["name"]



class PlaylistTrackForm(forms.ModelForm):
    class Meta:
        model = TrackAndOrder
        fields = ["track", "order"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if TrackAndOrder.objects.filter(playlist=instance.playlist,track=instance.track).exists():
            return TrackAndOrder.objects.get(playlist=instance.playlist, track=instance.track)
        if not instance.pk:
            # This is a new instance, set the order to the next available number
            max_order = TrackAndOrder.objects.filter(playlist=instance.playlist).aggregate(Max('order'))['order__max']
            if max_order is None:
                max_order = 0
            instance.order = max_order + 1
        else:
            max_count = TrackAndOrder.objects.filter(playlist=instance.playlist).count()+1
            instance.order = max_count
        if commit:
            instance.save()
        return instance


PlaylistTrackFormSet = inlineformset_factory(
    Playlist, TrackAndOrder, form=PlaylistTrackForm, fields=("track",), extra=1, can_delete=True
)
