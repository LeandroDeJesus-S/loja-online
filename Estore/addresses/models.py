from django.db import models
from django.contrib.auth import get_user_model

from store.models import Store

User = get_user_model()


class Address(models.Model):
    """the address related model.
    Args:
        street (CharField): the street name.
        state (CharField): the state name.
        city (CharField): the city name.
        postal_code (CharField): the postal code.
        
        stores (ManyToManyField): the relationship field to the stores.
        users (ManyToManyField): the relationship field to the users.
    """
    street = models.CharField(
        'Rua',
        max_length=100,
    )
    state = models.CharField(
        'Estado',
        max_length=45
    )
    city = models.CharField(
        'Cidade',
        max_length=45,
    )
    postal_code = models.CharField(
        'Código postal',
        max_length=10,
    )

    stores = models.ManyToManyField(Store, through="HasAddress")
    users = models.ManyToManyField(User, through="HasAddress")

    def __str__(self) -> str:
        """return the address like 'street, city - state / postal code'"""
        return f'{self.street}, {self.city} - {self.state} / {self.postal_code}'


class HasAddress(models.Model):
    """the tertiary entity of the relationship between address and store and user
    Args:
        number (CharField): the number of the code.
        complement (CharField): extra information of the address.
        user (ForeignKey): the relationship column that references user.
        store (ForeignKey): the relationship column that references the store.
        address (ForeignKey): the relationship column that references the address table.
    """
    number = models.CharField(
        'Número',
        max_length=10,
    )
    complement = models.CharField(
        "Complemento",
        max_length=100
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, null=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        """returns the number + the address representation"""
        return f'{self.number}, {self.address}'
