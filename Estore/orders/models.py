from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import ProductVariationOptionData
from utils.support.messages import OrderMessages

User = get_user_model()


class Order(models.Model):
    """The model that stores the orders of the users

    Args:
        total_items (PositiveIntegerField): the quantity of items purchased.
        total_amount (DecimalField): the total sum of the items.
        status (CharField): choices field with the order status.
        created_at (DateTimeField, AutoNow): the time when the order was created. Read only.
        user (ForeignKey): the user relationship field.
        variations (ManyToManyField): m2m field related to the ProductVariationOptionData model. Through fields: qtd (PositiveIntegerField)

        PENDING (str): status choice that represents a pending order.
        EXPIRED (str): status choice that represents an expired order.'
        CANCELED (str): status choice that represents a canceled order.
        PAID (str): status choice that represents a paid order.
    """

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    _MIN_ITEMS = 1
    _MIN_AMOUNT = 0

    PENDING = "PE"
    EXPIRED = "EX"
    CANCELED = "CA"
    PAID = "PA"

    STATUS_CHOICES = (
        (PENDING, _("Order pending")),
        (EXPIRED, _("Order expired")),
        (CANCELED, _("Order canceled")),
        (PAID, _("Order paid")),
    )

    total_items = models.PositiveIntegerField(
        _("Total items"),
        null=False,
        default=_MIN_ITEMS,
        validators=[
            MinValueValidator(
                _MIN_ITEMS,
                OrderMessages.ITEMS_INSUFFICIENT,
            ),
        ],
    )
    total_amount = models.DecimalField(
        _("Total amount"),
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(_MIN_AMOUNT),
        ],
        editable=False,
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, blank=False)
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name=_("User"),
    )
    variations = models.ManyToManyField(
        ProductVariationOptionData,
        through="OrderProductVariation",
        verbose_name=_("Variations"),
    )

    def __str__(self) -> str:
        """returns the order representation like
        'total items, total amount | status'
        """
        return f"{self.total_items}, {self.total_amount} | {self.status}"


class OrderProductVariation(models.Model):
    """The tertiary table to the products variation included to the
    user's order.

    Args:
        order (ForeignKey): the referenced order from the Order model.
        product_variation_option_data (ForeignKey): the reference to the product variation option data model.
        qtd (PositiveIntegerField): the quantity of a single variation.
    """

    class Meta:
        verbose_name = _("Order product variation")
        verbose_name_plural = _("Order product variations")

    _MIN_QTD = 1

    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Order"),
    )
    product_variation_option_data = models.ForeignKey(
        ProductVariationOptionData,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Product variation option data"),
    )
    qtd = models.PositiveIntegerField(
        _("Quantity"), validators=[MinValueValidator(_MIN_QTD)]
    )

    def __str__(self) -> str:
        """
        returns the representation like 'order, product variation option data | qtd'
        """
        return f"{self.order}, {self.product_variation_option_data} | {self.qtd}"
