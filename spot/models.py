from django.contrib.auth.models import AbstractUser
from django.db import models

# User model (Additional fields)
class User(AbstractUser):
    first_name = models.CharField(null=True, max_length=30)
    last_name = models.CharField(null=True, max_length=30)
    birthdate = models.DateField(blank=True, null=True)
    timezone = models.CharField(null=True, blank=True, max_length=50)
    last_uts = models.BigIntegerField(null=True, blank=True)

# Musical Genre model
class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)

# Artist model
class Artist(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tags = models.ManyToManyField(Genre)
    tags_fetched = models.BooleanField(default=False)

# Feelings stores in our db
class Feelings(models.Model):
    name = models.CharField(unique=True)
    score = models.FloatField(null=False)

# Diary Data
class DailySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_data")
    date = models.DateField(null=False)
    top_tracks = models.JSONField(default=dict, blank=True)
    total_scrobbles = models.IntegerField(default=0)
    top_artist = models.ManyToManyField(Artist)
    top_genres = models.ManyToManyField(Genre)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "date"), name="daily_data"
            )
        ]

# Diary Daily
class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_diary")
    user_entry = models.TextField(null=False)
    date = models.DateField(null=False)
    feeling = models.ForeignKey(Feelings, on_delete=models.CASCADE, related_name="daily_feeling")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "date"), name="diary_entry"
            )
        ]

# Pet
class PetState(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_pet")
    current_feeling = models.ForeignKey(Feelings, on_delete=models.CASCADE, related_name="pet_feeling")

# Pet Memory
class PetMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_pet_msg")
    date = models.DateTimeField(null=False)
    msg = models.TextField(null=False)