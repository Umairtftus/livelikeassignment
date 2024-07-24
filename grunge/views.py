import pdb

from django.db import transaction
from django.db.models import Max, F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Playlist, TrackAndOrder
from .forms import PlaylistForm, PlaylistTrackFormSet, PlaylistTrackForm


class PlaylistListView(ListView):
    model = Playlist
    template_name = "playlists/playlist_list.html"


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = "playlists/playlist_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PlaylistTrackForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PlaylistTrackForm(request.POST)
        if form.is_valid():
            track_and_order = form.save(commit=False)
            track_and_order.playlist = self.object
            track_and_order.save()
            return redirect('playlist_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(csrf_exempt, name='dispatch')
class PlaylistCreateView(CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = "playlists/playlist_form.html"
    success_url = reverse_lazy("playlist_list")

class PlaylistUpdateView(UpdateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = "playlists/playlist_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["tracks"] = PlaylistTrackFormSet(self.request.POST, instance=self.object)
        else:
            data["tracks"] = PlaylistTrackFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tracks = context["tracks"]
        curr_tracks = TrackAndOrder.objects.filter(playlist=self.object)

        # Track initial orders
        initial_orders = {track.id: track.order for track in curr_tracks}
        self.object = form.save()
        instances = tracks.save(commit=False)

        for instance in instances:
            if instance.id not in initial_orders:
                initial_orders[instance.id] = instance.order

        for instance in instances:
            if initial_orders[instance.id] >= instance.order:
                for track_id in initial_orders:
                    if initial_orders[track_id] >= instance.order:
                        initial_orders[track_id] -= 1
            elif initial_orders[instance.id] < instance.order:
                for track_id in initial_orders:
                    if initial_orders[track_id] <= instance.order:
                        initial_orders[track_id] += 1
            initial_orders[instance.id] = instance.order

        # Apply the updated orders
        for instance in instances:
            instance.order = initial_orders[instance.id]
            instance.playlist = self.object
            instance.save()

        # Save the formset
        tracks.save_m2m()

        # Adjust and save existing tracks not in instances
        for track in curr_tracks:
            if track.id not in initial_orders:
                track.order = initial_orders[track.id]
                track.save()

        return super().form_valid(form)


class PlaylistDeleteView(DeleteView):
    model = Playlist
    template_name = "playlists/playlist_confirm_delete.html"
    success_url = "/playlists/"

class PlaylistAddTracksView(UpdateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = "playlists/playlist_add_tracks.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["tracks"] = PlaylistTrackFormSet(self.request.POST, instance=self.object)
        else:
            data["tracks"] = PlaylistTrackFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tracks = context["tracks"]
        if tracks.is_valid():
            tracks.save()
        return super().form_valid(form)