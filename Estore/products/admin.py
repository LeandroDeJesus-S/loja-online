from django.contrib import admin

from .models import (
    Product,
    ProductVariation,
    ProductVariationFile,
    ProductCategory,
    ProductEvaluation,
    ProductEvaluationFile,
    ProductVariationOption,
    ProductVariationOptionData,
)
from .admin_inlines import VariationFileInline, VariationOptionInline


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): ...


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    inlines = [VariationOptionInline]


@admin.register(ProductVariationOption)
class ProductVariationOptionAdmin(admin.ModelAdmin): ...


@admin.register(ProductVariationOptionData)
class ProductVariationOptionDataAdmin(admin.ModelAdmin):
    list_display = ['price', 'stock', 'product', 'options_']
    inlines = [VariationFileInline]

    @admin.display(description='options')
    def options_(self, obj):
        return ', '.join([str(o) for o in obj.options.all()])


@admin.register(ProductVariationFile)
class ProductVariationFileAdmin(admin.ModelAdmin): ...


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin): ...


@admin.register(ProductEvaluation)
class ProductEvaluationAdmin(admin.ModelAdmin): ...


@admin.register(ProductEvaluationFile)
class ProductEvaluationFileAdmin(admin.ModelAdmin): ...
