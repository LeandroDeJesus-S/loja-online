from io import BytesIO

import pytest
from pytest_django.asserts import assertQuerySetEqual
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from products.models import (
    Product,
    ProductCategory,
    ProductVariation,
    ProductEvaluation,
    ProductVariationFile,
    ProductEvaluationFile,
)


@pytest.mark.django_db
def test_product_image_resized_post_save():
    """test if the image is resized successfully after save"""
    w, h = Product._IMAGE_MAX_DIM
    w += 10
    h += 10
    image = Image.new("RGB", (w, h), "white")
    buffer = BytesIO()
    image.save(buffer, "JPEG")
    image = SimpleUploadedFile("test_img.jpeg", buffer.getbuffer(), "image/jpeg")

    product = Product(
        name="test", image=image, description="lorem ipsum", base_price=100
    )

    product.save()
    product.refresh_from_db()

    new_size = product.image.width, product.image.height
    assert new_size == product._IMAGE_MAX_DIM


def test_product_str_method():
    """test the return of the __str__ method"""
    product = Product(name="test", description="lorem ipsum", base_price=100)
    assert str(product) == "test"


@pytest.mark.django_db
def test_product_slug_create_post_save(uploaded_img_file):
    """test if the slug filed is filled after the model to be saved"""
    product = Product(
        name="testing slug",
        image=uploaded_img_file,
        description="lorem ipsum",
        base_price=100,
    )
    assert not product.slug

    product.save()
    product.refresh_from_db()

    assert product.slug == "testing-slug"


@pytest.mark.django_db
def test_product_manager_available_func_return_products_with_available_stock(
    two_products_one_available,
):
    """test if the available method of the ProductManager returns
    the products with stock available.
    """
    all_products = Product.objects.all()
    available_products = Product.objects.available()
    assert all_products.count() == 2
    assert available_products.count() == 1


@pytest.mark.parametrize(
    "ordering,order_by",
    [
        ("new", "-pk"),
        ("less_price", "base_price"),
        ("greatest_price", "-base_price"),
        ("less_eval", "evaluation__evaluation"),
        ("greatest_eval", "-evaluation__evaluation"),
    ],
)
@pytest.mark.django_db
def test_product_manager_sort_return_the_products_sorted_correctly(ordering, order_by):
    result = Product.objects.sort(ordering)
    expected = Product.objects.order_by(order_by)
    assertQuerySetEqual(result, expected)


@pytest.mark.parametrize(
    "query,nres",
    [
        ("t-shirt", 2),
        ("doll", 1),
        ("female", 1),
        ("male", 1),
        ("kids", 1),
        ("clothes", 2),
        ("toys", 1),
        ("XL", 3),
    ],
)
@pytest.mark.django_db
def test_product_manager_search_returns_expected_results(query, nres, product_samples):
    """test if the search method of the manager returns the correct number of
    results according with the query.
    """
    result = Product.objects.search(query)
    assert result.count() == nres


def test_category_str_method(product):
    """test the return of the __str__ method"""
    cat = ProductCategory(name="test", product=product)
    assert str(cat) == "test"


def test_product_variation_str_method(product):
    """test the return of the __str__ method"""
    product_var = ProductVariation(
        name="color",
    )
    assert str(product_var) == "color"


def test_product_evaluation_str_method(product):
    evaluation = ProductEvaluation(
        evaluation=ProductEvaluation.BAD,
        comment="very bad",
        product=product,
    )
    assert str(evaluation) == f"{evaluation.evaluation} - {str(product)}"


def test_product_variation_file_str_method(
    product_variation_option_data, uploaded_img_file
):
    file = ProductVariationFile(
        file=uploaded_img_file,
        product_variation_data=product_variation_option_data,
    )
    assert str(file) == file.file.name
    file.file = None # type: ignore
    assert str(file) == "-"


def test_product_evaluation_file_str_method(uploaded_img_file):
    file = ProductEvaluationFile(
        file=uploaded_img_file,
    )
    assert str(file) == file.file.name
    file.file = None # type: ignore
    assert str(file) == "-"
