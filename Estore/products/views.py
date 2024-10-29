from typing import Any

from django.views.generic import ListView, DetailView

from .models import Product, ProductCategory
from .managers import ProductQuerySet


class ListProducts(ListView):
    template_name = "static/html/products/list_products.html"
    context_object_name = "products"
    model = Product
    queryset = Product.objects.available()
    paginate_by = 5
    ordering = '-pk'

    def get_queryset(self) -> ProductQuerySet:
        """returns the queryset ordered or filtered
        by the user search
        """
        qs: ProductQuerySet = super().get_queryset()  # type: ignore

        ordering = self.request.GET.get("ordering", "new").strip()
        search = self.request.GET.get("search", "")
        if not search:
            return qs.sort(ordering)

        return qs.search(search).sort(ordering)


class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "static/html/products/product_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """add the variations, variations data and categories to the
        context.
        """
        context = super().get_context_data(**kwargs)
        product = context['product']

        variations = []
                
        data = product.variation_options_data.prefetch_related('options', 'options__variation', 'data_files')
        for d in data:
            variation_options = [
                (option.variation.name, option.option_value) 
                for option in d.options.all()
            ]

            variations.append(variation_options)

        context['variations'] = variations
        context['variation_data'] = data
        context['categories'] = ProductCategory.objects.filter(product=product)
        return context
