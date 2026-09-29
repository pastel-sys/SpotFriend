from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# User model (Additional fields)
class User(AbstractUser):
    first_name = models.CharField(null=True, max_length=30)
    last_name = models.CharField(null=True, max_length=30)
    birthdate = models.DateField(blank=True, null=True)
    timezone = models.CharField(null=True, blank=True, max_length=50)

# Musical Genre model
class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)

# Artist model
class Artist(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tags = models.ManyToManyField(Genre)
    tags_fetched = models.BooleanField(default=False)

# Albums model
class Album(models.Model):
    name = models.TextField(null=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="album_owner")
    release_year = models.IntegerField(null=False)
    cover = models.URLField(null=False)
    genres = models.ManyToManyField(Genre)

# Track model
class Track(models.Model):
    name = models.CharField(max_length=150, null=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="album_track")
    duration = models.IntegerField()
    track_position = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["album", "track_position"], name="unique_relation_album_track_position")
        ]

# Rating model
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rating")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="user_track_rating")
    score = models.FloatField(validators=[MaxValueValidator(10), MinValueValidator(0)])
    created_at = models.DateField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "track"], name="unique_relation_user_track_rating")
        ]

# AlbumRating model
class AlbumRating(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="album_rating")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_album_rating")
    rating = models.FloatField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "album"], name="unique_relation_user_album")
        ]