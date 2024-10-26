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
    ProductEvaluation,
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
    """returns an variation option instance."""
    pvo = ProductVariationOption(
        option_value="blue",
        variation=product_variation,
    )
    pvo.save()
    pvo.refresh_from_db()
    return pvo


@pytest.fixture
def product_variation_option_data(
    db, product: Product, product_variation_option: ProductVariationOption
) -> ProductVariationOptionData:
    """returns an instance of a variation option data for `product`fixture
    instance."""
    pvod = ProductVariationOptionData(price=100, stock=1, product=product)
    pvod.save()
    pvod.options.add(product_variation_option)
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
        option_value="blue",
        variation=var[0],
    )

    var_value = ProductVariationOptionData(price=100, stock=0, product=pdt)
    var_value.save()
    var_value.options.add(var_opt)


@pytest.fixture
def product_samples(
    db,
    faker: Faker,
    uploaded_img_file: SimpleUploadedFile,
    admin_user,
    store: Store,
    settings,
):
    """populates the database with 3 product samples
    named 'Female T-Shirt', 'Male T-Shirt' and 'Kids doll'.
    2 categories named 'clothes' and 'toys'.
    2 variations named 'color' and 'size'.
    2 variation options to color (red, green) and 1 to size (XL).
    1 variation option data to each product (XL, red to female, XL and green to male and XL to kids).
    1 order to each product by the `admin_user` fixture with total_items eq 1 and status PAID.
    1 evaluation to each product (BAD, GOOD and GREAT respectively).
    """
    pdt_female, pdt_male, pdt_kids = Product.objects.bulk_create(
        [
            Product(
                name="Female T-Shirt",
                image=uploaded_img_file,
                base_price=50,
                slug="slug-1",
                description="t-shirt for girls",
            ),
            Product(
                name="Male T-Shirt",
                image=uploaded_img_file,
                base_price=100,
                slug="slug-2",
                description="clothes for men",
            ),
            Product(
                name="Kids doll",
                image=uploaded_img_file,
                base_price=150,
                slug="slug-3",
                description="toys for kids",
            ),
        ]
    )
    clothes_cat, toys_cat = ProductCategory.objects.bulk_create(
        [
            ProductCategory(name="Clothes"),
            ProductCategory(name="Toys"),
        ]
    )

    pdt_female.categories.add(clothes_cat)
    pdt_male.categories.add(clothes_cat)
    pdt_kids.categories.add(toys_cat)

    color_var, size_var = ProductVariation.objects.bulk_create(
        [
            ProductVariation(name="color"),
            ProductVariation(name="size"),
        ]
    )

    r, g, XL = ProductVariationOption.objects.bulk_create(
        [
            ProductVariationOption(option_value="red", variation=color_var),
            ProductVariationOption(option_value="green", variation=color_var),
            ProductVariationOption(option_value="XL", variation=size_var),
        ]
    )

    pdt_data = ProductVariationOptionData.objects.bulk_create(
        [
            ProductVariationOptionData(
                price=pdt_female.base_price, stock=1, product=pdt_female
            ),
            ProductVariationOptionData(
                price=pdt_male.base_price, stock=2, product=pdt_male
            ),
            ProductVariationOptionData(
                price=pdt_kids.base_price, stock=2, product=pdt_kids
            ),
        ]
    )
    pdt_fem_data, pdt_male_data, pdt_kids_data = pdt_data

    pdt_fem_data.options.add(XL, r)
    pdt_male_data.options.add(g, XL)
    pdt_kids_data.options.add(XL)

    orders = Order.objects.bulk_create(
        [
            Order(
                total_items=1,
                total_amount=pdt_fem_data.price,
                status=Order.PAID,
                user=admin_user,
            ),
            Order(
                total_items=1,
                total_amount=pdt_male_data.price,
                status=Order.PAID,
                user=admin_user,
            ),
            Order(
                total_items=1,
                total_amount=pdt_kids_data.price,
                status=Order.PAID,
                user=admin_user,
            ),
        ]
    )
    fem_order, male_order, kids_order = orders

    fem_order.variations.add(pdt_fem_data, through_defaults={"qtd": 1})
    male_order.variations.add(pdt_male_data, through_defaults={"qtd": 1})
    kids_order.variations.add(pdt_kids_data, through_defaults={"qtd": 1})

    ProductEvaluation.objects.bulk_create(
        [
            ProductEvaluation(evaluation=ProductEvaluation.BAD, product=pdt_female),
            ProductEvaluation(evaluation=ProductEvaluation.GOOD, product=pdt_male),
            ProductEvaluation(evaluation=ProductEvaluation.GREAT, product=pdt_kids),
        ]
    )
