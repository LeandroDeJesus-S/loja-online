from django.contrib import admin
from .models import Evaluation
from mediafiles.models import MediaFile


class FileInline(admin.TabularInline):
    model = MediaFile
    extra = 1
    exclude = ['product_variation']


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = [
        "evaluation",
        "created_at",
        "user",
        "order",
    ]
    inlines = [FileInline]

    @admin.display(description='Usuário')
    def user(self, obj):
        return obj.order.user
