from typing import Any
from django.db.models.query import QuerySet
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Avg
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product


class ListProducts(ListView):
    template_name = "static/html/products/list_products.html"
    context_object_name = "products"
    model = Product
    queryset = Product.objects.available()
    paginate_by = 5
    ordering = '-pk'

    ordering_dict = {
        "new": "-pk",
        "less_price": "avg",
        "greatest_price": "-avg",
        "less_eval": "product_variation__product_variation_order__order_evaluation",
        "greatest_eval": "-product_variation__product_variation_order__order_evaluation",
    }

    # def get_queryset(self) -> QuerySet[Any]:
    #     """returns the queryset ordered or filtered
    #     by the user search
    #     """
    #     qs = super().get_queryset()

    #     ordering = self.request.GET.get("ordering", "").strip()
        
    #     if not ordering or ordering not in self.ordering_dict.keys():
    #         ordering = "new"

    #     # if ordering in ['greatest_price', 'less_price']:
    #     #     return qs.order_by_mean_price(ordering_field)
    #     # return qs.all()

    #     search = self.request.GET.get("search", "")
    #     if not search:
    #         return self.sort_products(qs, ordering)

    #     sv = SearchVector(
    #         "name",
    #         "description",
    #         "product_variation__name",
    #         "product_variation__size",
    #         "categories__name",
    #     )
    #     q = SearchQuery(search)
    #     qs = qs.annotate(rank=SearchRank(sv, q)).filter(rank__gte=0.05)
    #     qs = self.sort_products(qs, ordering)
    #     return qs.prefetch_related(
    #         "product_variations__product_stores__store", 'product_variations'
    #     )

#     def sort_products(self, qs: QuerySet, ordering: str) -> QuerySet[Any]:
#         """manage the sorting of the products
        
#         Args:
#             qs (QuerySet): the products queryset.
#             ordering (str): the sorting method retrieved from request.
        
#         Returns:
#             QuerySet:
#         """
#         ordering_field = self.ordering_dict[ordering]
#         by_price = ordering in ['greatest_price', 'less_price']
#         if by_price:
#             return qs.order_by_mean_price(ordering_field)  # type: ignore
#         return qs.order_by(ordering_field)


# class ProductDetail(DetailView):
#     model = Product
#     context_object_name = "product"
#     template_name = "static/html/products/product_detail.html"

#     def get_queryset(self) -> QuerySet[Any]:
#         qs = super().get_queryset()
#         return qs.prefetch_related(
#             "product_variations__files",
#             "product_variations__product_stores__store",
#             "categories",
#         )
