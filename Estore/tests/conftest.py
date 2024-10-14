from decimal import Decimal
from io import BytesIO

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from products.models import Product, ProductVariation


@pytest.fixture
def dumb_upload_img_file() -> InMemoryUploadedFile:
    """return an img object instance of the InMemoryUploadedFile class"""
    image = Image.new('RGB', (200, 300), 'green')
    buffer = BytesIO()
    image.save(buffer, 'JPEG')

    file = InMemoryUploadedFile(
        buffer,
        None,
        'upload.jpeg',
        'image/jpeg',
        buffer.getbuffer().nbytes,
        None
    )
    return file


@pytest.fixture
def dumb_product(db, dumb_upload_img_file: InMemoryUploadedFile) -> Product:
    """returns an instance of the product model.

    Args:
        dumb_upload_file (InMemoryUploadedFile): file to use like the logo

    Returns:
        Product: instance of a product
    """
    pdt = Product(
        name="short",
        description="short test",
        thumbnail=dumb_upload_img_file
    )
    pdt.save()
    pdt.refresh_from_db()
    return pdt


@pytest.fixture
def dumb_product_variation(db, dumb_product: Product) -> ProductVariation:
    """returns an instance of the product variation model.

    Args:
        dumb_product (Product): a product model instance.

    Returns:
        ProductVariation: 
    """
    var = ProductVariation(
        name="short variation",
        size="G",
        color="red",
        price=Decimal("10"),
        product=dumb_product,
    )
    var.save()
    var.refresh_from_db()
    return var
