# Generated by Django 3.1.5 on 2024-07-24 08:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('grunge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('name', models.CharField(help_text='The playlist name', max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TrackAndOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('order', models.PositiveIntegerField(blank=True, help_text='The Track number on the playlist', null=True)),
                ('playlist', models.ForeignKey(help_text='The playlist of the track', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='playlist_tracks', to='grunge.playlist')),
                ('track', models.ForeignKey(help_text='Track refers to the playlist', on_delete=django.db.models.deletion.CASCADE, related_name='track', to='grunge.track')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.AddIndex(
            model_name='playlist',
            index=models.Index(fields=['name'], name='grunge_play_name_ed1809_idx'),
        ),
        migrations.AddIndex(
            model_name='trackandorder',
            index=models.Index(fields=['order', 'playlist', 'track'], name='grunge_trac_order_c3f511_idx'),
        ),
        migrations.AddConstraint(
            model_name='trackandorder',
            constraint=models.UniqueConstraint(fields=('playlist', 'track'), name='unique_track'),
        ),
    ]
