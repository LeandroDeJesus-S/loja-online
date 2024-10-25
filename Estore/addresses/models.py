from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from utils.support.messages import AddressMessages
from utils.support import regex

User = get_user_model()


class Address(models.Model):
    """the address related model.

    Args:
        street (CharField): the street name.
        city (CharField): the city name.
        state (CharField): the state abbr (e.g: US to united states).
        country (CharField): the country abbr (e.g: CA to California)
        postal_code (CharField): the postal code.
    """

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    street = models.CharField(
        _("Street"),
        max_length=100,
        validators=[
            RegexValidator(regex.BASIC_TEXT)
        ],
    )
    city = models.CharField(
        _("City"),
        max_length=45,
        validators=[
            RegexValidator(regex.BASIC_TEXT),
        ],
    )
    state = models.CharField(
        _("State"),
        max_length=2,
        validators=[
            RegexValidator(
                regex.ISO3166_1_ALPHA2,
                AddressMessages.INVALID_STATE,
            ),
        ],
        help_text='Ex.: CA'
    )
    country = models.CharField(
        _("Country"),
        max_length=2,
        help_text="Ex.: US",
        validators=[
            RegexValidator(
                regex.ISO3166_1_ALPHA2,
                AddressMessages.INVALID_COUNTRY,
            ),
        ],
    )
    postal_code = models.CharField(
        _("Postal code"),
        max_length=10,
        validators=[
            RegexValidator(regex.POSTAL_CODE)
        ]
    )

    def __str__(self) -> str:
        """return the address like 'street, city - state / country | postal code'"""
        return f"{self.street}, {self.city} - {self.state} / {self.country} | {self.postal_code}"


class UserAddress(models.Model):
    """the intermediary entity of the relationship between address and
    user and user that contains the complement fields.

    Args:
        number (CharField): user's address number.
        complement (CharField): user's address complement.
        user (ForeignKey): the user owner of the address.
        address (ForeignKey): the address model reference.
    """

    class Meta:
        verbose_name = _("User's address")
        verbose_name_plural = _("User's addresses")

    number = models.CharField(
        _("Number"),
        max_length=10,
        validators=[
            RegexValidator(r'^[A-Za-z0-9]+$'),
        ],
    )
    complement = models.CharField(
        _("Complement"),
        max_length=100,
        blank=True,
        validators=[
            RegexValidator(regex.BASIC_TEXT),
        ],
    )
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name=_("User"),
        related_name='user_address',
        related_query_name='user_address',
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Address"),
        related_name='address_user_addresses',
        related_query_name='address_user_address',
    )

    def __str__(self) -> str:
        """returns the comma separated number and the complement """
        return f"{self.number}, {self.complement}"
