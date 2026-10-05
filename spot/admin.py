from django.contrib import admin
from spot.models import User, Genre, Artist, Album, Track, Rating, AlbumRating

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "birthdate", "timezone", "password"]
    exclude = ["lastfm_session_key"]

class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

class ArtistAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "tags_fetched"]
    filter_horizontal = ["tags"]

class AlbumAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "artist", "release_year", "cover"]
    filter_horizontal = ["genres"]

class TrackAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "album", "duration", "track_position"]

class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "track", "score", "created_at"]

class AlbumRatingAdmin(admin.ModelAdmin):
    list_display = ["id", "album", "user", "rating"]

admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(AlbumRating, AlbumRatingAdmin)