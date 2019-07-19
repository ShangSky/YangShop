from django.contrib import admin
from .models import UserProfile, Address


@admin.register(UserProfile)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
