from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
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
        return self.name


class Order(models.Model):
    """the model that stores the orders of the users
    Args:
        qtd (PositiveIntegerField): the quantity of items purchased.
        created_at (DateTimeField): the time when the order was created. Read only.
        status (ForeignKey): the relationship field to the status model.
        user (ForeignKey): the user relationship field.
        product_variation (ForeignKey): the product variation relationship field.
    """

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    _STRIPE_PI_ID_MAX_LEN = _STRIPE_METHOD_ID_MAX_LEN = 32

    qtd = models.PositiveIntegerField(
        "Qtd.",
        null=False,
        default=1,
    )
    created_at = models.DateTimeField(
        "Criada em",
        auto_now_add=True,
        editable=False,
    )
    stripe_payment_id = models.CharField(
        max_length=_STRIPE_PI_ID_MAX_LEN,
        unique=True,
        validators=[
            RegexValidator(
                r"^pi_[A-Za-z0-9]+$",
                OrderMessages.INVALID_STRIPE_PAYMENT_ID,
            ),
        ],
    )
    stripe_payment_method_id = models.CharField(
        max_length=_STRIPE_METHOD_ID_MAX_LEN,
        validators=[
            RegexValidator(
                r"^pm_[A-Za-z0-9]+$",
                OrderMessages.INVALID_STRIPE_PAYMENT_METHOD,
            ),
        ],
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
