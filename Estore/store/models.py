from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator

from utils.support.messages import StoreMessages, GenericMessages
from utils.support.func import resize_image
from products.models import ProductVariation


class StoreHasProduct(models.Model):
    """the tertiary model to the relationship between store and products.

    Args:
        store (ForeignKey): store relationship field
        product (ForeignKey): product relationship field
        qtd (PositiveIntegerField): the quantity of the product stocked
    """

    class Meta:
        verbose_name = "Loja com produto adquirido"
        verbose_name_plural = "Lojas com produto adquirido"

    store = models.ForeignKey(
        "Store",
        on_delete=models.CASCADE,
        verbose_name="Loja",
    )
    product = models.ForeignKey(
        ProductVariation,
        on_delete=models.CASCADE,
        verbose_name="Produto",
    )
    qtd = models.PositiveIntegerField(
        "Estoque",
        null=False,
        default=0,
    )

    def __str__(self) -> str:
        """returns the representation like 'store, product | qtd'"""
        return f"{self.store}, {self.product} | {self.qtd}"


class Store(models.Model):
    """model that represents a store entity

    Args:
        name (CharField): the store name; unique; only letters, digits, space and "_"; max len 45, min 2.
        slogan (CharField): the store page slogan.
        logo (ImageField): the logo image of the store.
        cnpj (CharField): the store CNPJ.
    """

    class Meta:
        verbose_name = "Loja"
        verbose_name_plural = "Lojas"

    _NAME_MIN_LEN, _NAME_MAX_LEN = 2, 45
    _NAME_LEN_ERR_MSG = GenericMessages.INVALID_LEN.format_map(
        {"field": "nome", "min_len": _NAME_MIN_LEN, "max_len": _NAME_MAX_LEN}
    )

    _SLOGAN_MAX_LEN = 100
    _CNPJ_LEN = 14
    _LOGO_MAX_SIZE = 360, 360

    name = models.CharField(
        "Nome",
        max_length=_NAME_MAX_LEN,
        blank=False,
        unique=True,
        validators=[
            RegexValidator(r"^[\w ]+$", StoreMessages.INVALID_NAME),
            MinLengthValidator(_NAME_MIN_LEN, _NAME_LEN_ERR_MSG),
        ],
        error_messages={"invalid": StoreMessages.INVALID_NAME},
    )
    slogan = models.CharField(max_length=_SLOGAN_MAX_LEN, blank=False, unique=True)
    logo = models.ImageField(upload_to="store/logos")
    cnpj = models.CharField(
        max_length=_CNPJ_LEN,
        validators=[
            RegexValidator(r"^\d+$", StoreMessages.INVALID_CNPJ),
            MinLengthValidator(_CNPJ_LEN, StoreMessages.INVALID_CNPJ),
        ],
        error_messages={"invalid": StoreMessages.INVALID_CNPJ},
    )
    products = models.ManyToManyField(
        ProductVariation,
        through=StoreHasProduct,
        related_name="product_stores",
        related_query_name="product_store",
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        """resizes the logo post saved"""
        super().save(*args, **kwargs)
        resize_image(self.logo.path, *self._LOGO_MAX_SIZE)
