from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from store.models import Store
from utils.support.messages import AddressMessages
from utils.support import regex

User = get_user_model()


class Address(models.Model):
    """the address related model.

    Args:
        street (CharField): the street name.
        state (CharField): the state abbr (e.g: US to united states).
        city (CharField): the city name.
        postal_code (CharField): the postal code.
        country (CharField): the country abbr (e.g: CA to California)
        stores (ManyToManyField): the relationship field to the stores.
        users (ManyToManyField): the relationship field to the users.
    """

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    street = models.CharField(
        "Rua",
        max_length=100,
        validators=[
            RegexValidator(regex.BASIC_TEXT)
        ],
    )
    state = models.CharField(
        "Estado",
        max_length=2,
        validators=[
            RegexValidator(
                regex.ISO3166_1_ALPHA2,
                AddressMessages.INVALID_STATE,
            ),
        ],
        help_text='Ex.: CA'
    )
    city = models.CharField(
        "Cidade",
        max_length=45,
        validators=[
            RegexValidator(regex.BASIC_TEXT),
        ],
    )
    postal_code = models.CharField(
        "Código postal",
        max_length=10,
        validators=[
            RegexValidator(regex.POSTAL_CODE)
        ]
    )
    country = models.CharField(
        "País",
        max_length=2,
        help_text="Ex.: US",
        validators=[
            RegexValidator(
                regex.ISO3166_1_ALPHA2,
                AddressMessages.INVALID_COUNTRY,
            ),
        ],
    )
    stores = models.ManyToManyField(Store, through="HasAddress")
    users = models.ManyToManyField(User, through="HasAddress")

    def __str__(self) -> str:
        """return the address like 'street, city - state / country | postal code'"""
        return f"{self.street}, {self.city} - {self.state} / {self.country} | {self.postal_code}"


class HasAddress(models.Model):
    """the tertiary entity of the relationship between address and store and user
    Args:
        number (CharField): the number of the code.
        complement (CharField): extra information of the address.
        user (ForeignKey): the relationship column that references user.
        store (ForeignKey): the relationship column that references the store.
        address (ForeignKey): the relationship column that references the address table.
    """

    class Meta:
        verbose_name = "Endereço atribuído"
        verbose_name_plural = "Endereços atribuídos"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(user__isnull=True, store__isnull=False) | # type: ignore
                      models.Q(user__isnull=False, store__isnull=True) |
                      models.Q(user__isnull=False, store__isnull=False),
                name='chk_has_address_fks_not_given_together'
            )
        ]

    number = models.CharField(
        "Número",
        max_length=10,
        validators=[
            RegexValidator(r'^[A-Za-z0-9]+$'),
        ],
    )
    complement = models.CharField(
        "Complemento",
        max_length=100,
        blank=True,
        validators=[
            RegexValidator(regex.BASIC_TEXT),
        ],
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.DO_NOTHING,
        null=True,
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self) -> str:
        """returns the number + the address representation"""
        return f"{self.number}, {self.address}"
