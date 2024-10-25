from io import BytesIO

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from products.models import Product, ProductCategory, ProductVariation


@pytest.mark.django_db
def test_product_thumbnail_resized_post_save():
    """test if the thumbnail is resized successfully after save"""
    w, h = Product._IMAGE_MAX_DIM
    w += 10
    h += 10
    image = Image.new("RGB", (w, h), "white")
    buffer = BytesIO()
    image.save(buffer, "JPEG")
    image = InMemoryUploadedFile(
        buffer, None, "thumb.jpeg", "image/jpeg", buffer.getbuffer().nbytes, None
    )

    product = Product(
        name="test",
        image=image,
        description='lorem ipsum',
        base_price=100
    )

    product.save()
    product.refresh_from_db()

    new_size = product.image.width, product.image.height
    assert new_size == product._IMAGE_MAX_DIM


def test_product_str_method():
    """test the return of the __str__ method"""
    product = Product(
        name="test",
        description='lorem ipsum',
        base_price=100
    )    
    assert str(product) == 'test'


@pytest.mark.django_db
def test_product_slug_create_post_save(uploaded_img_file):
    """test if the slug filed is filled after the model to be saved"""
    product = Product(
        name="testing slug",
        image=uploaded_img_file,
        description='lorem ipsum',
        base_price=100
    )
    assert not product.slug
    
    product.save()
    product.refresh_from_db()

    assert product.slug == 'testing-slug'


@pytest.mark.django_db
def test_product_manager_available_func_return_products_with_available_stock(two_products_one_available):
    """test if the available method of the ProductManager returns
    the products with stock available.
    """
    all_products = Product.objects.all()
    available_products = Product.objects.available()
    assert all_products.count() == 2
    assert available_products.count() == 1


def test_category_str_method(product):
    """test the return of the __str__ method"""
    cat = ProductCategory(name='test', product=product)
    assert str(cat) == 'test'


def test_product_variation_str_method(product):
    """test the return of the __str__ method"""
    product_var = ProductVariation(
        name="color",
    )
    assert str(product_var) == 'color'
