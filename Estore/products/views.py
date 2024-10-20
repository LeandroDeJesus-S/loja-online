from typing import Any
from django.db.models.query import QuerySet
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, ProductVariation
from mediafiles.models import MediaFile


class ListProducts(ListView):
    template_name = "static/html/products/list_products.html"
    context_object_name = "products"
    model = Product
    queryset = Product.listing.all()
    paginate_by = 5

    ordering_dict = {
        "new": "-id",
        "less_price": "product_variation__price",
        "greatest_price": "-product_variation__price",
        "less_eval": "product_variation__product_variation_order__order_evaluation",
        "greatest_eval": "-product_variation__product_variation_order__order_evaluation",
    }

    def get_queryset(self) -> QuerySet[Any]:
        """returns the queryset ordered or filtered
        by the user search
        """
        qs = super().get_queryset()

        ordering = self.request.GET.get("ordering", "").strip()
        if not ordering:
            ordering = 'new'

        ordering_field = self.ordering_dict[ordering]

        search = self.request.GET.get("search", "")
        if not search:
            return qs.order_by(ordering_field)

        sv = SearchVector(
            "name",
            "description",
            "product_variation__name",
            "product_variation__size",
            "categories__name",
        )
        q = SearchQuery(search)
        qs = (
            qs.annotate(rank=SearchRank(sv, q))
            .filter(rank__gte=.05)
            .distinct()
            
        )
        return qs.order_by(ordering_field)


class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "static/html/products/product_detail.html"
