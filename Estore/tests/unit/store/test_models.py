from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import pytest
from PIL import Image
from store.models import Store


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
