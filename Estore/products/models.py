from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    MinValueValidator,
    validate_image_file_extension,
)
from django.utils.translation import gettext_lazy as _

from utils.support.messages import (
    GenericMessages,
    ProductMessages,
    CategoryMessages,
)
from utils.support.func import resize_image
from utils.support.validators import FileSizeValidator
from utils.support import regex

from .managers import ProductManager


class Product(models.Model):
    """model that represent a product

    Args:
        name (CharField): the product name. Min len 2, max 45
        base_price (FloatField): base price to display on list the products.
        slug (SlugField): the product slug. Auto created using the product name before to save.
        image (ImageField): the product image to display on list products.
        description (TextField): a description about the product.

        categories (ManyToManyField): m2m field to the product categories model.
        variations (ManyToManyField): m2m field to the product variations model.
    """

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    _MIN_NAME_LEN, _MAX_NAME_LEN = 2, 100

    _IMAGE_MAX_DIM = 360, 360
    _MAX_IMG_SIZE = 5 * 1024**2  # 5MB

    _MAX_DESC_CHAR = 500

    objects: ProductManager = ProductManager()

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
            RegexValidator(
                regex.BASIC_TEXT,
                ProductMessages.INVALID_NAME,
            ),
        ],
        error_messages={"invalid": ProductMessages.INVALID_NAME},
        help_text=_(
            f"min {_MIN_NAME_LEN}, max {_MAX_NAME_LEN}. Letters, numbers, spaces and _"
        ),
    )
    base_price = models.FloatField(
        _("Base price"),
        help_text=_("price displayed on the linting of the products"),
        validators=[MinValueValidator(0, ProductMessages.INVALID_PRICE)],
    )
    image = models.ImageField(
        _("Image"),
        upload_to="products/thumbs/%Y/%m",
        validators=[
            validate_image_file_extension,
            FileSizeValidator(
                size=_MAX_IMG_SIZE,
                msg=GenericMessages.FILE_SIZE_EXCEEDED,
            ),
        ],
        help_text=_("image displayed on listing the products."),
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        editable=False,
    )
    description = models.TextField(
        _("Description"),
        max_length=_MAX_DESC_CHAR,
        blank=True,
        help_text=_(f"Max {_MAX_DESC_CHAR} char."),
    )
    categories = models.ManyToManyField(
        "ProductCategory",
        verbose_name=_("Categories"),
    )
    variations = models.ManyToManyField(
        "ProductVariation",
        verbose_name=_("Product variations"),
        related_name='products',
        related_query_name='product',
        blank=True
    )

    def __str__(self) -> str:
        """returns the variation name."""
        return self.name

    def save(self, *args, **kwargs):
        """add the slug by name and resize the thumbnail"""
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
        if self.image:
            resize_image(self.image.path, *self._IMAGE_MAX_DIM)


class ProductCategory(models.Model):
    """the model to store categories for the products

    Args:
        name (CharField): the name of the category. Letters, digits and spaces or "_".
    """

    class Meta:
        verbose_name = _("Product category")
        verbose_name_plural = _("Product categories")

    name = models.CharField(
        _("Name"),
        max_length=45,
        validators=[
            RegexValidator(regex.BASIC_TEXT, CategoryMessages.INVALID_NAME),
        ],
        blank=False,
        error_messages={"invalid": CategoryMessages.INVALID_NAME},
        help_text=_("The name must be alphanumeric separated by spaces or _"),
    )

    def __str__(self) -> str:
        """returns the category name."""
        return self.name


class ProductEvaluation(models.Model):
    """the model to store the an evaluation of an user to a product.

    Args:
        evaluation (CharField): the evaluation choice of the Evaluations.
        comment (TextField): extra comments to the evaluation.
        created_at (DateTimeField): date when the evaluation was created.
        product (ForeignKey): the reference field to the product model.

        TERRIBLE (str): evaluation choice
        BAD (str): evaluation choice
        OK (str): evaluation choice
        GOOD (str): evaluation choice
        GREAT (str): evaluation choice
    """

    class Meta:
        verbose_name = _("Product evaluation")
        verbose_name_plural = _("Product evaluations")

    _MAX_DESC_CHAR = 255

    TERRIBLE = "1"
    BAD = "2"
    OK = "3"
    GOOD = "4"
    GREAT = "5"

    EVALUATION_CHOICES = (
        (TERRIBLE, _("Terrible")),
        (BAD, _("Bad")),
        (OK, _("Ok")),
        (GOOD, _("Good")),
        (GREAT, _("Great")),
    )

    evaluation = models.CharField(
        _("Evaluation"),
        max_length=1,
        choices=EVALUATION_CHOICES,
    )
    comment = models.TextField(
        _("Commentary"),
        max_length=_MAX_DESC_CHAR,
        null=True,
        blank=True,
        help_text=_(f"Max. {_MAX_DESC_CHAR} chars."),
    )
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, editable=False
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Product"),
        related_name='evaluations',
        related_query_name="evaluation",
    )

    def __str__(self) -> str:
        """returns the representation in 'evaluation - product'"""
        return f"{self.evaluation} - {self.product}"


class ProductEvaluationFile(models.Model):
    """model that stores the files from a evaluation

    Args:
        file (FileField): the attached file to the evaluation.
    """

    class Meta:
        verbose_name = _("Product evaluation file")
        verbose_name_plural = _("Product evaluation files")

    _MAX_FILE_SIZE = 5 * 1024**2  # 5MB
    _FILE_MAX_DIM = 480, None

    file = models.FileField(
        upload_to="products/evaluation_files/%Y/%m",
        blank=True,
        null=True,
        validators=[
            validate_image_file_extension,
            FileSizeValidator(
                size=_MAX_FILE_SIZE,
                msg=GenericMessages.FILE_SIZE_EXCEEDED,
            ),
        ],
    )

    def __str__(self) -> str:
        """returns the file name or '-' if no file"""
        return self.file.name if self.file else "-"


class ProductVariation(models.Model):
    """Store a type of variation name ex.: size, color, etc.

    Args:
        name (CharField): an unique variation type name.

        options (QuerySet): generated field from m2m relationship with ProductVariationOption.
    """

    class Meta:
        verbose_name = _("Product variation")
        verbose_name_plural = _("Product variations")

    name = models.CharField(
        _("Name"),
        max_length=45,
        blank=False,
        unique=True,
        validators=[
            RegexValidator(regex.BASIC_TEXT, GenericMessages.INVALID_NAME),
        ],
        help_text=_("the product variation name. (ex.: color, size)"),
    )

    def __str__(self) -> str:
        """returns the product variation name."""
        return self.name


class ProductVariationOption(models.Model):
    """Represents an option for a product variation for example to
    a variation named 'color' has a variation option value 'blue' and a
    variation name 'size' has a variation option value 'XL'.
    
    Args:
        option_value (CharField): the value to a variation (ex.: blue, XL).
        variation (ForeignKey): the reference to the variation.
    """

    class Meta:
        verbose_name = _("Product variation option")
        verbose_name_plural = _("Product variation options")

    option_value = models.CharField(
        _("Option value"),
        max_length=100,
        help_text=_(
            "The variation option value (ex.: blue, XL)"
        )
    )
    variation = models.ForeignKey(
        ProductVariation,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Variation"),
        related_name='options',
        related_query_name='option',
    )

    def __str__(self) -> str:
        """returns the option value"""
        return self.option_value


class ProductVariationOptionData(models.Model):
    """model to store data about a variation option.

    Args:
        price (DecimalField(10,2)): the option/s price.
        stock (PositiveIntegerField): the stock available for the option/s
        options (ManyToManyField): the referenced field to the options.
        product (ForeignKey): the reference to the product
    """
    class Meta:
        verbose_name = _('product variation option data')
        verbose_name_plural = _('product variation option data')

    _PRICE_MAX_DIGITS = 10
    _PRICE_DECIMAL_PLACES = 2
    _MIN_PRICE = Decimal("0")

    price = models.DecimalField(
        _("Price"),
        max_digits=_PRICE_MAX_DIGITS,
        decimal_places=_PRICE_DECIMAL_PLACES,
        validators=[MinValueValidator(_MIN_PRICE, ProductMessages.INVALID_PRICE)],
    )
    stock = models.PositiveIntegerField(
        _("Stock"),
    )
    options = models.ManyToManyField(
        ProductVariationOption,
        verbose_name=_("Options"),
        related_name='options_data',
        related_query_name='option_data',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Product"),
        related_name='variation_options_data',
        related_query_name='variation_option_data',
    )

    def __str__(self) -> str:
        """returns the price and the stock separated by one space"""
        self.product
        var = ', '.join([str(v) for v in self.options.all()])
        return f'{self.product} | {var}'


class ProductVariationFile(models.Model):
    """model that stores the files from the product variation options

    Args:
        file (FileField): the attached file to the variation.
        product_variation_data (ForeignKey): reference field to the variation option data.
    """

    class Meta:
        verbose_name = _("Product variation file")
        verbose_name_plural = _("Product variation files")

    _MAX_FILE_SIZE = 5 * 1024**2  # 5MB
    _FILE_MAX_DIM = 480, None

    file = models.FileField(
        upload_to="products/variation_files/%Y/%m",
        blank=True,
        null=True,
        validators=[
            validate_image_file_extension,
            FileSizeValidator(
                size=_MAX_FILE_SIZE,
                msg=GenericMessages.FILE_SIZE_EXCEEDED,
            ),
        ],
    )
    product_variation_data = models.ForeignKey(
        ProductVariationOptionData,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Product variation data"),
        related_name="data_files",
        related_query_name="data_file",
    )

    def __str__(self) -> str:
        """returns the file name or '-' if no file"""
        return self.file.name if self.file else "-"
