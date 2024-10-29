from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.http import HttpRequest

from products.models import ProductVariationOptionData
from .utils import CartSessionManager


@require_GET
def manage_cart(request, option_pk: str | int):
    referer = request.META.get("HTTP_REFERER", "home")

    cart_manager = CartSessionManager(request, option_pk)
    cart_manager.manage()
    return redirect(referer)


@require_GET
def show_cart(request: HttpRequest):
    """show the products of the cart"""
    cart = request.session.get("cart", {})

    products = (
        ProductVariationOptionData.objects
        .filter(pk__in=cart.keys())
        .prefetch_related("options")
    )
    options = []
    for option_data, data in zip(products, cart.values()):
        data = {
            "product": option_data,
            "qtd": data["qtd"],
            "amount": data["qtd"] * option_data.price,
        }
        options.append(data)

    return render(
        request,
        "static/html/cart/cart.html",
        {"product_variation_options_data": options},
    )
