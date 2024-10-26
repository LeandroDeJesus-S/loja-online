import os
from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from products.models import (
    Product,
    ProductCategory,
    ProductVariationOptionData,
    ProductVariationOption,
    ProductVariation,
)
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
    expected_products = Product.objects.available()
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
    response = client.get(reverse("home") + f"?ordering={ordering}")

    response_products = response.context["products"]
    expected_products = Product.objects.sort(ordering)

    assertQuerySetEqual(response_products, expected_products)


@pytest.mark.parametrize(
    "search",
    ["t-shirt", "female", "male", "kids", "var 1"],
)
def test_list_products_search(client: Client, product_samples, search: str, settings):
    response = client.get(reverse("home") + f"?search={search}")
    response_products = response.context["products"]

    sv = SearchVector(
        "name",
        "description",
        "variations__option__option_value",
        "categories__name",
    )
    q = SearchQuery(search)

    expected_products = (
        Product.objects.annotate(rank=SearchRank(sv, q))
        .filter(rank__gte=0.05)
        .distinct()
    )
    assert response.status_code == HTTPStatus.OK
    assertQuerySetEqual(response_products, expected_products.order_by("-pk"))


@pytest.mark.django_db
def test_product_detail_context(client: Client, product_samples):
    """test if the context data is correctly"""
    product = Product.objects.get(name='Female T-Shirt')
    
    response = client.get(reverse("products:product_detail", args=(product.slug,)))
    context = response.context

    variations = context["variations"]
    variations_data = context["variation_data"]
    categories = context["categories"]

    expected_variations = [[('color', 'red'), ('size', 'XL')]]
    expected_variations_data = product.variation_options_data.all()
    expected_categories = product.categories.all()

    assert variations == expected_variations
    assertQuerySetEqual(variations_data, expected_variations_data)
    assertQuerySetEqual(categories, expected_categories)
