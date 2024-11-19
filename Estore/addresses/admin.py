from django.contrib import admin
from . models import Address, UserAddress


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    ...


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    ...
