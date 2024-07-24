# Generated by Django 3.1.5 on 2024-07-24 07:45

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
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(help_text='The playlist name', max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.RemoveField(
            model_name='album',
            name='id',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='id',
        ),
        migrations.RemoveField(
            model_name='track',
            name='id',
        ),
        migrations.AlterField(
            model_name='album',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='UUID'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='UUID'),
        ),
        migrations.AlterField(
            model_name='track',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='UUID'),
        ),
        migrations.CreateModel(
            name='TrackAndOrder',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('order', models.PositiveIntegerField(blank=True, help_text='The Track number on the playlist', null=True)),
                ('playlist', models.ForeignKey(help_text='The playlist of the track', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='playlist', to='grunge.playlist')),
                ('track', models.ForeignKey(help_text='Track refers to the playlist', on_delete=django.db.models.deletion.CASCADE, related_name='track', to='grunge.track')),
            ],
            options={
                'ordering': ('playlist', 'track', 'order'),
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
