from django.contrib import admin

from .models import Store
from addresses.models import HasAddress


class StoreAddressInline(admin.StackedInline):
    model = HasAddress
    exclude = ['user']
    extra = 0


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'cnpj', 'slogan', 'logo'
    ]
    inlines = [
        StoreAddressInline
    ]
