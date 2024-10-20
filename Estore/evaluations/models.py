from django.db import models
from django.utils.translation import gettext_lazy as _

from orders.models import Order


class Evaluation(models.Model):
    """the model to store the user's evaluations
    
    Args:
        evaluation (CharField): the evaluation choice of the Evaluations.
        description (TextField): the description of the evaluation.
        created_at (DateTimeField): date when the evaluation was created.
        order (ForeignKey): the reference field to the order model.
        
        TERRIBLE (str): evaluation choice
        BAD (str): evaluation choice
        OK (str): evaluation choice
        GOOD (str): evaluation choice
        GREAT (str): evaluation choice
    """

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
    
    _MAX_DESC_CHAR = 255

    TERRIBLE = "1"
    BAD = "2"
    OK = "3"
    GOOD = "4"
    GREAT = "5"

    EVALUATION_CHOICES = (
        (TERRIBLE,  _("Terrible")),
        (BAD,  _("Bad")),
        (OK,  _("Ok")),
        (GOOD,  _("Good")),
        (GREAT,  _("Great")),
    )

    evaluation = models.CharField(
        "Avaliação",
        max_length=1,
        choices=EVALUATION_CHOICES,
    )
    description = models.TextField(
        'Descrição',
        max_length=_MAX_DESC_CHAR,
        null=True,
        blank=True,
        help_text=_(f'Max. {_MAX_DESC_CHAR} chars.')
    )
    created_at = models.DateTimeField(
        "Criada em",
        auto_now_add=True,
        editable=False
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        verbose_name='Pedido',
        related_query_name='order_evaluation'
    )

    def __str__(self) -> str:
        """returns the representation like 'user - order | evaluation'"""
        return f'{self.order.user} - {self.order} | {self.evaluation}'
