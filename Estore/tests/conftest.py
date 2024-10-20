from decimal import Decimal
from io import BytesIO

import pytest
from addresses.models import Address
from django.core.files.uploadedfile import InMemoryUploadedFile
from evaluations.models import Evaluation
from faker import Faker
from orders.models import Order, OrderStatus
from PIL import Image
from products.models import Product, ProductVariation
from store.models import Store


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
        name="test store",
        slogan="store to tests",
        logo=memory_upload_img_file,
        cnpj="57207196000107",
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
    """returns an Order instance using `processing_order` fixture."""
    e = Evaluation(evaluation=Evaluation.OK, order=processing_order)
    e.save()
    return e


@pytest.fixture
def address(db):
    """return an instance of Address model."""
    addrss = Address(
        street="street",
        state="ST",
        city="city",
        postal_code="1234567890",  # TODO: alter on create validation
        country="CO",
    )
    addrss.save()
    return addrss


@pytest.fixture
def two_products_one_available(
    db, store: Store, product_variation: ProductVariation, memory_upload_img_file
):
    """creates two products which just one has available stock"""

    store.products.add(product_variation, through_defaults={"qtd": 1})

    pdt = Product(
        name="short2", description="short test2", thumbnail=memory_upload_img_file
    )
    pdt.save()
    var = ProductVariation(
        name="short variation 2",
        size="M",
        color="red",
        price=Decimal("10"),
        product=pdt,
    )
    var.save()

    store.products.add(var, through_defaults={"qtd": 0})


@pytest.fixture
def product_sorting_samples(
    db,
    faker: Faker,
    memory_upload_img_file,
    processing_order_status,
    admin_user,
    store: Store,
):
    """populates the database with 2 product samples
    having 'prod 1' with price equals to 100 and a bad evaluation
    and the 'prod 2' with price 50 and a god evaluation
    """
    pdts = Product.objects.bulk_create([
        Product(
            name="prod 1",
            thumbnail=memory_upload_img_file,
            slug='slug-1',
        ),
        Product(
            name="prod 2",
            thumbnail=memory_upload_img_file,
            slug='slug-2',
        ),
    ])
    pdt_vars = ProductVariation.objects.bulk_create([
        ProductVariation(
            name="prod var 1",
            size=faker.random_letter(),
            color=faker.color_name(),
            price=100,
            product=pdts[0],
            slug='slug-1',
        ),
        ProductVariation(
            name="prod var 2",
            size=faker.random_letter(),
            color=faker.color_name(),
            price=50,
            product=pdts[1],
            slug='slug-2',
        ),
    ])

    orders = Order.objects.bulk_create([
        Order(
            qtd=1,
            status=processing_order_status,
            user=admin_user,
            product_variation=pdt_vars[0],
        ),
        Order(
            qtd=1,
            status=processing_order_status,
            user=admin_user,
            product_variation=pdt_vars[1],
        ),
    ])
    Evaluation.objects.bulk_create([
        Evaluation(
            evaluation=Evaluation.BAD,
            order=orders[0],
        ),
        Evaluation(
            evaluation=Evaluation.GOOD,
            order=orders[1],
        ),
    ])

    store.products.add(*pdt_vars, through_defaults={'qtd': 1})
