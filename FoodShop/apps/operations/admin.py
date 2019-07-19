from django.contrib import admin
from .models import UserFav


@admin.register(UserFav)
class UserFavAdmin(admin.ModelAdmin):
    pass
