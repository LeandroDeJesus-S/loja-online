from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    MinValueValidator,
    validate_image_file_extension,
)

from utils.support.messages import GenericMessages, ProductMessages, CategoryMessages
from utils.support.func import resize_image
from utils.support.validators import FileSizeValidator


class ProductVariation(models.Model):
    """Store the variation of products.

    Args:
        name (CharField): the variation name.
        size (CharField): the size information (e.g: G, XL).
        color (CharField): information of colors.
        slug (SlugField): slug auto generated using the variation name.
        price (DecimalField(10,2)): the product price.
        product (ForeignKey): related field to the Product model.
    """

    class Meta:
        verbose_name = "Variação"
        verbose_name_plural = "Variações"

    _PRICE_MAX_DIGITS = 10
    _PRICE_DECIMAL_PLACES = 2
    _MIN_PRICE = Decimal("0")

    name = models.CharField(
        "Nome",
        max_length=45,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(r"^[\w ]+$"),
        ],
    )
    size = models.CharField(
        "Tamanho",
        max_length=4,
        blank=False,
        help_text="Ex.: G, GG, XGG",
        validators=[
            RegexValidator(r"^[\w ]+$"),
        ],
    )
    color = models.CharField(
        "Cor",
        max_length=20,
        blank=False,
        validators=[
            RegexValidator(r"^[A-Za-z ]+$"),
        ],
        help_text="apenas letras e espaços, sem acentuações (Ex.: azul e rosa)",
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        editable=False,
    )
    price = models.DecimalField(
        "Preço",
        max_digits=_PRICE_MAX_DIGITS,
        decimal_places=_PRICE_DECIMAL_PLACES,
        blank=False,
        validators=[MinValueValidator(_MIN_PRICE)],
        error_messages={"invalid": ProductMessages.INVALID_PRICE},
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.DO_NOTHING,
        verbose_name="Produto",
    )

    def __str__(self) -> str:
        """returns the product variation name."""
        return self.name

    def save(self, *args, **kwargs):
        """set the slug before to save."""
        print("slug before to save:", self.slug)
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Category(models.Model):
    """the model to store categories for the products

    Args:
        name (CharField): the name of the category. Letters, digits and spaces or "_".
        cat_products (ManyToManyField): related name field to the Product model.
    """

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    name = models.CharField(
        "Nome",
        max_length=45,
        validators=[
            RegexValidator(r"^[\w ]+$", CategoryMessages.INVALID_NAME),
        ],
        blank=False,
        error_messages={"invalid": CategoryMessages.INVALID_NAME},
        help_text="O nome deve ser alfanumérico separados por espaços ou _",
    )

    def __str__(self) -> str:
        """returns the category name."""
        return self.name


class Product(models.Model):
    """model that represent a product

    Args:
        name (CharField): the product name. Min len 2, max 45
        slug (SlugField): the product slug. Auto created using the product name before to save.
        categories (ManyToManyField): the related name to the Category model relationship.
        description (CharField): a short description about the variation.
    """

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    _MIN_NAME_LEN, _MAX_NAME_LEN = 2, 45

    _THUMBNAIL_MAX_DIM = 360, 360
    _MAX_THUMB_SIZE = 5 * 1024  # 5KB

    name = models.CharField(
        "Nome",
        max_length=_MAX_NAME_LEN,
        blank=False,
        unique=True,
        validators=[
            MinLengthValidator(
                _MIN_NAME_LEN,
                GenericMessages.INVALID_LEN.format_map(
                    {
                        "field": "nome",
                        "min_len": _MIN_NAME_LEN,
                        "max_len": _MAX_NAME_LEN,
                    },
                ),
            ),
            RegexValidator(r"^[\w ]+$", ProductMessages.INVALID_NAME),
        ],
        error_messages={"invalid": ProductMessages.INVALID_NAME},
        help_text=f"min {_MIN_NAME_LEN}, max {_MAX_NAME_LEN}. Letras, números, espaços e _",
    )
    slug = models.SlugField(unique=True, blank=True, editable=False)
    thumbnail = models.ImageField(
        upload_to="products/thumbs/%Y-%m",
        validators=[
            validate_image_file_extension,
            FileSizeValidator(
                size=_MAX_THUMB_SIZE,
                msg=GenericMessages.FILE_SIZE_EXCEEDED,
            ),
        ],
    )
    categories = models.ManyToManyField(
        Category,
        related_name="cat_products",
        related_query_name="cat_product",
        verbose_name="Categoria",
    )
    description = models.TextField(
        "Descrição",
        max_length=500,
        blank=True,
        help_text="Max 500 char.",
    )

    def __str__(self) -> str:
        """returns the variation name."""
        return self.name

    def save(self, *args, **kwargs):
        """add the slug by name and resize the thumbnail"""
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
        resize_image(self.thumbnail.path, *self._THUMBNAIL_MAX_DIM)
