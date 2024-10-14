from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import pytest
from PIL import Image
from store.models import Store, StoreHasProductVariation


def test_store_str():
    """test the return of the __str__  method from store model."""
    store = Store(
        name="test",
        slogan="test",
        cnpj="74473068000124",
    )
    assert str(store) == "test"


@pytest.mark.django_db
def test_logo_resized_post_save():
    """test if the logo is resized successfully after save"""
    w, h = Store._LOGO_MAX_DIM
    w += 10
    h += 10
    image = Image.new("RGB", (w, h), "white")
    buffer = BytesIO()
    image.save(buffer, "JPEG")
    logo = InMemoryUploadedFile(
        buffer, None, "logo.jpeg", "image/jpeg", buffer.getbuffer().nbytes, None
    )

    store = Store(
        name="test",
        slogan="test",
        logo=logo,
        cnpj="74473068000124",
    )

    store.save()
    store.refresh_from_db()

    new_size = store.logo.width, store.logo.height
    assert new_size == store._LOGO_MAX_DIM


@pytest.mark.django_db
def test_store_has_product_variation_str(dumb_product_variation, dumb_upload_img_file):
    """test the __str__ method from StoreHasProduct model.

    Args:
        dumb_product_variation (ProductVariation): instance of the model ProductVariation.
    """
    store = Store.objects.create(
        name="test",
        slogan="test",
        cnpj="74473068000124",
        logo=dumb_upload_img_file,
    )
    qtd = 1
    store_prod = StoreHasProductVariation(store=store, product=dumb_product_variation, qtd=qtd)
    assert str(store_prod) == f"{str(store)}, {str(dumb_product_variation)} | {qtd}"
