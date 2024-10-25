from django.db import models
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    validate_image_file_extension,
)
from django.utils.translation import gettext_lazy as _

from utils.support.messages import StoreMessages, GenericMessages
from utils.support.func import resize_image
from utils.support.validators import FileSizeValidator, validate_cnpj


class Store(models.Model):
    """model to store base settings of the store.

    Args:
        name (CharField): the store name; unique; only letters, digits, space and "_"; max len 45, min 2.
        slogan (CharField): the store page slogan.
        logo (ImageField): the logo image of the store.
        cnpj (CharField): the store CNPJ.
        created_at (DatetimeField): the time when the store was created. Defaults add the now time.
    """

    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")

    _NAME_MIN_LEN, _NAME_MAX_LEN = 2, 45
    _NAME_LEN_ERR_MSG = _(
        GenericMessages.INVALID_LEN.format_map(
            {"field": "nome", "min_len": _NAME_MIN_LEN, "max_len": _NAME_MAX_LEN}
        )
    )

    _SLOGAN_MAX_LEN = 100
    _CNPJ_LEN = 14
    _LOGO_MAX_DIM = 360, 360
    _LOGO_MAX_SIZE = 5 * 1024**2  # 5MB

    name = models.CharField(
        _("Name"),
        max_length=_NAME_MAX_LEN,
        blank=False,
        unique=True,
        validators=[
            RegexValidator(r"^[\w \.]+$", StoreMessages.INVALID_NAME),
            MinLengthValidator(_NAME_MIN_LEN, _NAME_LEN_ERR_MSG),
        ],
        error_messages={"invalid": StoreMessages.INVALID_NAME},
    )
    slogan = models.CharField(
        max_length=_SLOGAN_MAX_LEN,
        blank=False,
        unique=True,
        help_text=_(f"max: {_SLOGAN_MAX_LEN} chars."),
    )
    logo = models.ImageField(
        upload_to="store/logos",
        validators=[
            FileSizeValidator(
                size=_LOGO_MAX_SIZE, msg=GenericMessages.FILE_SIZE_EXCEEDED
            ),
            validate_image_file_extension,
        ],
        help_text="Max: 5KB",
        null=True,
        blank=True,
    )
    cnpj = models.CharField(
        max_length=_CNPJ_LEN,
        validators=[
            RegexValidator(r"^\d+$", StoreMessages.INVALID_CNPJ, "invalid"),
            MinLengthValidator(_CNPJ_LEN, StoreMessages.INVALID_CNPJ),
            validate_cnpj,
        ],
        error_messages={"invalid": StoreMessages.INVALID_CNPJ},
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
    )

    def __str__(self) -> str:
        """returns the store name."""
        return self.name

    def save(self, *args, **kwargs):
        """resizes the logo post saved"""
        super().save(*args, **kwargs)
        if self.logo:
            resize_image(self.logo.path, *self._LOGO_MAX_DIM)
