from decimal import Decimal
from io import BytesIO

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile
from orders.models import Order, OrderStatus
from PIL import Image
from products.models import Product, ProductVariation
from evaluations.models import Evaluation
from store.models import Store
from addresses.models import Address


@pytest.fixture
def memory_upload_img_file() -> InMemoryUploadedFile:
    """return an img object instance of the InMemoryUploadedFile class"""
    image = Image.new("RGB", (200, 300), "green")
    buffer = BytesIO()
    image.save(buffer, "JPEG")

    file = InMemoryUploadedFile(
        buffer, None, "upload.jpeg", "image/jpeg", buffer.getbuffer().nbytes, None
    )
    return file


@pytest.fixture
def store(db, memory_upload_img_file):
    """return an instance of Store model with name `test store` and 
    no products.
    """
    s = Store(
        name='test store',
        slogan='store to tests',
        logo=memory_upload_img_file,
        cnpj='16.545.829/0001-00',
    )
    s.save()
    return s


@pytest.fixture
def product(db, memory_upload_img_file: InMemoryUploadedFile) -> Product:
    """returns an instance of the product model.

    Args:
        dumb_upload_file (InMemoryUploadedFile): file to use like the logo

    Returns:
        Product: instance of a product
    """
    pdt = Product(
        name="short", description="short test", thumbnail=memory_upload_img_file
    )
    pdt.save()
    pdt.refresh_from_db()
    return pdt


@pytest.fixture
def product_variation(db, product: Product) -> ProductVariation:
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
        product=product,
    )
    var.save()
    var.refresh_from_db()
    return var


@pytest.fixture
def processing_order_status(db) -> OrderStatus:
    """returns a status instance with name 'processing'"""
    status = OrderStatus(name="processing")
    status.save()
    return status


@pytest.fixture
def processing_order(
    db,
    processing_order_status: OrderStatus,
    product_variation: ProductVariation,
    admin_user,
) -> Order:
    """return an instance of a order using `processing_order_status`
    and `dumb_product_variation` fixtures
    """
    order = Order(
        qtd=2,
        status=processing_order_status,
        user=admin_user,
        product_variation=product_variation,
    )
    order.save()
    return order


@pytest.fixture
def processing_order_evaluation(db, processing_order: Order) -> Evaluation:
    """returns an Order instance using `processing_order` fixture.
    """
    e = Evaluation(
        evaluation=Evaluation.OK,
        order=processing_order
    )
    e.save()
    return e


@pytest.fixture
def address(db):
    """return an instance of Address model."""
    addrss = Address(
        street='street',
        state='ST',
        city='city',
        postal_code='12345687890',  # TODO: alter on create validation
        country='CO',
    )
    addrss.save()
    return addrss