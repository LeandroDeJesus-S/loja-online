from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from products.models import ProductVariation
from utils.support.messages import OrderMessages

User = get_user_model()


class OrderStatus(models.Model):
    """the model to stores order status
    Args:
        name (CharField): the order status name.
    """

    class Meta:
        verbose_name = "Status de pedido"
        verbose_name_plural = "Status de pedidos"

    name = models.CharField(
        "Nome",
        unique=True,
        max_length=45,
        validators=[
            RegexValidator(
                r"^[\w ]+$",
                OrderMessages.INVALID_ORDER_STATUS_NAME,
            )
        ],
        error_messages={"invalid": OrderMessages.INVALID_ORDER_STATUS_NAME},
    )

    def __str__(self) -> str:
        """returns the order status name"""
        return self.name


class Order(models.Model):
    """the model that stores the orders of the users
    Args:
        qtd (PositiveIntegerField): the quantity of items purchased.
        created_at (DateTimeField, AutoNow): the time when the order was created. Read only.
        status (ForeignKey): the relationship field to the status model.
        user (ForeignKey): the user relationship field.
        product_variation (ForeignKey): the product variation relationship field.
    """

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    qtd = models.PositiveIntegerField(
        "Qtd.",
        null=False,
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )
    created_at = models.DateTimeField(
        "Criada em",
        auto_now_add=True,
        editable=False,
    )
    status = models.ForeignKey(
        OrderStatus,
        on_delete=models.DO_NOTHING,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name="Usuário",
    )
    product_variation = models.ForeignKey(
        ProductVariation,
        on_delete=models.DO_NOTHING,
        verbose_name="Variação",
    )

    def __str__(self) -> str:
        """returns the order representation like 'username | product, qtd - status'
        """
        usr = self.user.username
        prod = self.product_variation
        status = self.status.name
        return f"{usr} | {prod}, {self.qtd} - {status}"

    def order_value(self, as_int: bool = False) -> int | Decimal:
        """returns the total value of the order.

        Args:
            as_int (bool, optional): if is True return the value in integer. Defaults to False.

        Returns:
            int | Decimal: the value as int or Decimal.
        """
        value = self.qtd * self.product_variation.price
        if as_int:
            return int(value * 100)
        return value
