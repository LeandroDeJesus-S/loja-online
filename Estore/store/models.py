from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator

from utils.support.messages import StoreMessages, GenericMessages
from utils.support.func import resize_image


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

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        """resizes the logo post saved"""
        super().save(*args, **kwargs)
        resize_image(self.logo.path, *self._LOGO_MAX_SIZE)
