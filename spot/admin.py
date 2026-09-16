from django.contrib import admin
from spot.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "birthdate", "password"]

admin.site.register(User, UserAdmin)
