import pytest
from django.urls import reverse
from django.test.client import Client
from products.models import ProductVariationOptionData

from django.contrib.messages.storage.fallback import FallbackStorage
from cart.views import manage_cart


@pytest.mark.django_db
def test_show_cart_context_options(client: Client, product_samples):
    """test if the correct options are sent to the context"""
    cart = {
        "1": {"qtd": 1},
        "2": {"qtd": 1},
    }
    for oid in cart.keys():
        client.get(reverse("cart:manage", args=(oid,)) + "?action=add")

    response = client.get(reverse("cart:show_cart"))

    context = response.context

    products = ProductVariationOptionData.objects.filter(
        pk__in=cart.keys()
    ).prefetch_related("options")
    expected_options = []
    for option_data, data in zip(products, cart.values()):
        data = {
            "product": option_data,
            "qtd": data["qtd"],
            "amount": data["qtd"] * option_data.price,
        }
        expected_options.append(data)

    assert expected_options == context["product_variation_options_data"]


@pytest.mark.parametrize('action,pre_cart,expected_cart', [
    ('add', {'1': {'qtd': 1}}, {'1': {'qtd': 2}}),
    ('remove', {'1': {'qtd': 1}}, {}),
    ('increase', {'1': {'qtd': 1}}, {'1': {'qtd': 2}}),
    ('decrease', {'1': {'qtd': 2}}, {'1': {'qtd': 1}}),
])
def test_manage_cart_view(rf, product_samples, action, pre_cart, expected_cart):
    """test if the operations (add, remove, increase, decrease) of the cart in 
    the session is working as expected.
    """
    option_id = "1"

    opt = ProductVariationOptionData.objects.get(pk=option_id)
    opt.stock = 2
    opt.save()
    opt.refresh_from_db()

    class DumbSession(dict):
        def save(self): ...

    request = rf.get(
        reverse("cart:manage", args=(option_id,)) + f"?action={action}",
    )
    request.session = DumbSession()
    request.session['cart'] = pre_cart

    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    manage_cart(request, option_id)

    cart = request.session["cart"]
    assert cart == expected_cart
