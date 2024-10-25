from decimal import Decimal
from io import BytesIO

import pytest
from addresses.models import Address
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from orders.models import Order
from PIL import Image
from products.models import (
    Product,
    ProductVariation,
    ProductCategory,
    ProductVariationOption,
    ProductVariationOptionData,
)
from store.models import Store


@pytest.fixture
def uploaded_img_file() -> SimpleUploadedFile:
    """return an img object instance of the SimpleUploadedFile class"""
    image = Image.new("RGB", (200, 300), "green")
    buffer = BytesIO()
    image.save(buffer, "JPEG")

    file = SimpleUploadedFile("test_img.jpeg", buffer.getbuffer(), "image/jpeg")
    return file


@pytest.fixture
def store(db, uploaded_img_file):
    """return an instance of Store model with name `test store` and
    no products.
    """

    s = Store(
        name="test store",
        slogan="store to tests",
        logo=uploaded_img_file,
        cnpj="57207196000107",
    )
    s.save()
    return s


@pytest.fixture
def product(db, uploaded_img_file: SimpleUploadedFile) -> Product:
    """returns an instance of the product model.

    Args:
        dumb_upload_file (SimpleUploadedFile): file to use like the logo

    Returns:
        Product: instance of a product
    """
    pdt = Product(
        name="short", 
        description="short test", 
        image=uploaded_img_file,
        base_price=100,
    )
    pdt.save()
    pdt.refresh_from_db()
    return pdt


@pytest.fixture
def product_variation(db, product: Product) -> ProductVariation:
    """returns an instance of the product variation model.

    Args:
        product (Product): a product model instance.

    Returns:
        ProductVariation:
    """
    var = ProductVariation(
        name="color",
    )
    var.save()
    var.refresh_from_db()
    return var


@pytest.fixture
def product_variation_option(db, product_variation: ProductVariation):
    """returns an variation option instance.
    """
    pvo = ProductVariationOption(
        option_value='blue',
        variation=product_variation,
    )
    pvo.save()
    pvo.refresh_from_db()
    return pvo


@pytest.fixture
def product_variation_option_data(db, product: Product) -> ProductVariationOptionData:
    """returns an instance of a variation option data for `product`fixture
    instance."""
    pvod = ProductVariationOptionData(
        price=100,
        stock=1,
        product=product
    )
    pvod.save()
    return pvod


@pytest.fixture
def pending_order(
    db,
    product_variation: ProductVariation,
    admin_user,
) -> Order:
    """return an instance of a order with `pending` status"""
    order = Order(
        total_items=2,
        total_amount=100,
        status=Order.PENDING,
        user=admin_user,
    )
    order.save()
    return order


@pytest.fixture
def address(db):
    """return an instance of Address model."""
    addrss = Address(
        street="street",
        state="ST",
        city="city",
        postal_code="60714-610",
        country="CO",
    )
    addrss.save()
    return addrss


@pytest.fixture
def two_products_one_available(
    db, 
    product: Product, 
    product_variation: ProductVariation, 
    product_variation_option: ProductVariationOption,
    product_variation_option_data: ProductVariationOptionData,
    uploaded_img_file,
):
    """creates two products which just one has available stock"""
    product_variation_option_data.options.add(product_variation_option)
    

    pdt = Product(
        name="short2", 
        description="short test2", 
        image=uploaded_img_file,
        base_price=100,
    )
    pdt.save()
    
    var = ProductVariation.objects.get_or_create(
        name="color",
    )

    var_opt = ProductVariationOption.objects.create(
        option_value='blue',
        variation=var[0],
    )

    var_value = ProductVariationOptionData(
        price=100,
        stock=0,
        product=pdt
    )
    var_value.save()
    var_value.options.add(var_opt)


# @pytest.fixture
# def product_samples(
#     db,
#     faker: Faker,
#     uploaded_img_file: SimpleUploadedFile,
#     processing_order_status: OrderStatus,
#     admin_user,
#     store: Store,
#     settings,
# ):
#     """populates the database with 3 product samples
#     named 'Female T-Shirt', 'Male T-Shirt' and 'Kids doll'.
#     3 product variations (one for each product) named 'prod var 1/2/3'
#     and prices 50, 100 and 150.

#     each one have an order and an evaluation (BAD, GOOD and GREAT respectively).
#     """
#     pdts = Product.objects.bulk_create(
#         [
#             Product(
#                 name="Female T-Shirt",
#                 thumbnail=uploaded_img_file,
#                 slug="slug-1",
#             ),
#             Product(
#                 name="Male T-Shirt",
#                 thumbnail=uploaded_img_file,
#                 slug="slug-2",
#             ),
#             Product(
#                 name="Kids doll",
#                 thumbnail=uploaded_img_file,
#                 slug="slug-3",
#             ),
#         ]
#     )
#     clothes_cat, toys_cat = Category.objects.bulk_create(
#         [
#             Category(name="Clothes"),
#             Category(name="Toys"),
#         ]
#     )
#     for pdt in pdts:
#         cat = toys_cat if "kid" in pdt.name.lower() else clothes_cat
#         pdt.categories.add(cat)

#     pdt_vars = ProductVariation.objects.bulk_create(
#         [
#             ProductVariation(
#                 name=f"prod var {idx + 1}",
#                 size=faker.random_letter(),
#                 color=faker.color(color_format="hex"),
#                 price=50 * (idx + 1),
#                 product=pdt,
#                 slug=f"slug-{idx}",
#             )
#             for idx, pdt in enumerate(pdts)
#         ]
#     )

#     orders = Order.objects.bulk_create(
#         [
#             Order(
#                 qtd=1,
#                 status=processing_order_status,
#                 user=admin_user,
#                 product_variation=pdt_var,
#             )
#             for pdt_var in pdt_vars
#         ]
#     )
#     Evaluation.objects.bulk_create(
#         [
#             Evaluation(
#                 evaluation=Evaluation.BAD,
#                 order=orders[0],
#             ),
#             Evaluation(
#                 evaluation=Evaluation.GOOD,
#                 order=orders[1],
#             ),
#             Evaluation(
#                 evaluation=Evaluation.GREAT,
#                 order=orders[2],
#             ),
#         ]
#     )

#     store.products.add(*pdt_vars, through_defaults={"qtd": 1})
