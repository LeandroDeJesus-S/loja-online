from __future__ import annotations

from django.db.models import Manager, QuerySet
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


class ProductQuerySet(QuerySet):
    def available(self) -> ProductQuerySet:
        """returns the products where at least one variation has the
        stock greatest or equal to 1.
        """
        return self.filter(variation_option_data__stock__gte=1).distinct()

    def search(self, query: str) -> ProductQuerySet:
        """makes a fulltext search using the given query string."""
        sv = SearchVector(
            "name",
            "description",
            "variation_option_data__options__option_value",
            "categories__name",
        )
        q = SearchQuery(query)
        qs = self.annotate(rank=SearchRank(sv, q)).filter(rank__gte=0.05)
        return qs.distinct()

    def sort(self, ordering: str):
        """return the products sorted by the given ordering method.
        
        Args:
            ordering (str): any of: "new", "less_price", "greatest_price", "less_eval", "greatest_eval"
        """
        sort_dict = {
            "new": "-pk",
            "less_price": "base_price",
            "greatest_price": "-base_price",
            "less_eval": "evaluation__evaluation",
            "greatest_eval": "-evaluation__evaluation",
        }

        ordering_field = sort_dict.get(ordering, "-pk")
        return self.order_by(ordering_field)


class ProductManager(Manager):
    def get_queryset(self) -> ProductQuerySet:
        return ProductQuerySet(self.model, using=self._db)
    
    def available(self) -> ProductQuerySet:
        """returns the products where at least one variation has the
        stock greatest or equal to 1.
        """
        return self.get_queryset().available()

    def search(self, query: str) -> ProductQuerySet:
        """makes a fulltext search using the given query string."""
        return self.get_queryset().search(query)


    def sort(self, ordering: str):
        """return the products sorted by the given ordering method.
        
        Args:
            ordering (str): any of: "new", "less_price", "greatest_price", "less_eval", "greatest_eval"
        """
        return self.get_queryset().sort(ordering)
