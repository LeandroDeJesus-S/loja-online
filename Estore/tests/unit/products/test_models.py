from io import BytesIO

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from products.models import Product, Category, ProductVariation


@pytest.mark.django_db
def test_product_thumbnail_resized_post_save():
    """test if the thumbnail is resized successfully after save"""
    w, h = Product._THUMBNAIL_MAX_DIM
    w += 10
    h += 10
    image = Image.new("RGB", (w, h), "white")
    buffer = BytesIO()
    image.save(buffer, "JPEG")
    thumb = InMemoryUploadedFile(
        buffer, None, "thumb.jpeg", "image/jpeg", buffer.getbuffer().nbytes, None
    )

    product = Product(
        name="test",
        thumbnail=thumb,
        description='lorem ipsum',
    )

    product.save()
    product.refresh_from_db()

    new_size = product.thumbnail.width, product.thumbnail.height
    assert new_size == product._THUMBNAIL_MAX_DIM


def test_product_str_method():
    """test the return of the __str__ method"""
    product = Product(
        name="test",
        description='lorem ipsum',
    )    
    assert str(product) == 'test'


@pytest.mark.django_db
def test_product_slug_create_post_save(memory_upload_img_file):
    """test if the slug filed is filled after the model to be saved"""
    product = Product(
        name="testing slug",
        thumbnail=memory_upload_img_file,
        description='lorem ipsum',
    )
    assert not product.slug
    
    product.save()
    product.refresh_from_db()

    assert product.slug == 'testing-slug'


def test_category_str_method():
    """test the return of the __str__ method"""
    cat = Category(name='test')
    assert str(cat) == 'test'


@pytest.mark.django_db
def test_product_variation_slug_create_post_save(product):
    """test if the slug filed is filled after the model to be saved"""
    product_var = ProductVariation(
        name="testing slug",
        size='P',
        color='red',
        price='20.5',
        product=product,
    )
    assert not product_var.slug
    
    product_var.save()
    product_var.refresh_from_db()

    assert product_var.slug == 'testing-slug'


def test_product_variation_str_method(product):
    """test the return of the __str__ method"""
    product_var = ProductVariation(
        name="testing slug",
        size='P',
        color='red',
        price='20.5',
        product=product,
    )
    assert str(product_var) == 'testing slug'
