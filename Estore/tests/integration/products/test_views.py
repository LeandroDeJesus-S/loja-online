import os
from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from products.models import Product
from pytest_django.asserts import assertTemplateUsed, assertQuerySetEqual


@pytest.mark.django_db
def test_list_products_template(client: Client):
    """test if list_products return the correct template"""
    response = client.get(reverse("home"))
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "static/html/products/list_products.html")


@pytest.mark.django_db
def test_list_products_context(client: Client, two_products_one_available):
    """test if list_products return the correct products on context"""
    response = client.get(reverse("home"))
    context = response.context

    context_products = context["products"]
    expected_products = Product.listing.all()
    assertQuerySetEqual(context_products, expected_products)


@pytest.mark.parametrize(
    "ordering",
    [
        "new",
        "less_price",
        "greatest_price",
        "less_eval",
        "greatest_eval",
    ],
)
def test_list_products_ordering(client: Client, product_samples, ordering):
    """test if the sorting of the products by user form is working as expected."""
    ordering_dict = {
        "new": "-id",
        "less_price": "product_variation__price",
        "greatest_price": "-product_variation__price",
        "less_eval": "product_variation__product_variation_order__order_evaluation",
        "greatest_eval": "-product_variation__product_variation_order__order_evaluation",
    }

    response = client.get(reverse("home") + f'?ordering={ordering}')

    response_products = response.context["products"]
    expected_products = Product.objects.order_by(ordering_dict[ordering])

    assertQuerySetEqual(response_products, expected_products)


@pytest.mark.parametrize(
    'search',
    ['t-shirt', 'female', 'male', 'kids', 'var 1'],
)
def test_list_products_search(client: Client, product_samples, search: str, settings):
    response = client.get(reverse('home') + f'?search={search}')
    response_products = response.context['products']

    sv = SearchVector(
        "name",
        "description",
        "product_variation__name",
        "product_variation__size",
        "categories__name",
    )
    q = SearchQuery(search)

    expected_products = (
        Product.listing
        .annotate(rank=SearchRank(sv, q))
        .filter(rank__gte=.05)
        .distinct()
    )
    assert response.status_code == HTTPStatus.OK
    assertQuerySetEqual(response_products, expected_products.order_by('-id'))
