from typing import Any
from django.contrib import admin
from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import Input
from django.http import HttpRequest

from .models import Product, Category, ProductVariation
from store.models import StoreHasProductVariation
from mediafiles.models import MediaFile


class ProductVariationFileInline(admin.TabularInline):
    model = MediaFile
    extra = 1
    exclude = ['evaluation']


class VariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1
    verbose_name = 'Variação'
    verbose_name_plural = 'Variações'


class CategoryInline(admin.TabularInline):
    model = Product.categories.through
    extra = 1
    verbose_name = 'Categoria'
    verbose_name_plural = 'Categorias'


class StoreInline(admin.TabularInline):
    model = StoreHasProductVariation
    extra = 1


class ProductVariationForm(ModelForm):
    class Meta:
        model = ProductVariation
        exclude = ()
        widgets = {
            'color': Input({'type': 'color'})
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "thumbnail",
    ]
    inlines = [VariationInline, CategoryInline]
    exclude = ["variations", "categories"]


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "size",
        "color",
        "price",
    ]
    inlines = [StoreInline, ProductVariationFileInline]
    form = ProductVariationForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
