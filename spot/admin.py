from django.contrib import admin
from spot.models import User, Genre, Artist, Feelings, DailySummary, DiaryEntry, PetState, PetMessage

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "birthdate", "password"]

class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

class ArtistAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "tags_fetched"]
    filter_horizontal = ["tags"]

class FeelingsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "score"]

class DailySummaryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "date", "top_tracks", "total_scrobbles"]
    filter_horizontal = ["top_artist", "top_genres"]

class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "date", "feeling"]
    exclude = ["user_entry"]
 
class PetStateAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "current_feeling"]

class PetMessageAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "date", "msg"]

admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Feelings, FeelingsAdmin)
admin.site.register(DailySummary, DailySummaryAdmin)
admin.site.register(DiaryEntry, DiaryEntryAdmin)
admin.site.register(PetState, PetStateAdmin)
admin.site.register(PetMessage, PetMessageAdmin)