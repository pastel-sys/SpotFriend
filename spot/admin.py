from django.contrib import admin
from spot.models import User, Genre, Artist, Album, Track, Rating, AlbumRating

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "birthdate", "timezone", "password"]
    filter_horizontal = ["favorite_albums"]
    exclude = ["lastfm_session_key"]

class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

class ArtistAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "get_tags","tags_fetched"]
    filter_horizontal = ["tags"]

    def get_tags(self, obj):
        tag_list = []
        for tag in obj.tags.all():
            tag_list.append(tag.name)
        return tag_list

class AlbumAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "artist", "release_year", "get_tags", "cover"]
    filter_horizontal = ["genres"]

    def get_tags(self, obj):
        tag_list = []
        for tag in obj.genres.all():
            tag_list.append(tag.name)
        return tag_list

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