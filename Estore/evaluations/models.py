from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from orders.models import Order

User = get_user_model()


class Evaluation(models.Model):
    """the model to store the user's evaluations
    
    Args:
        evaluation (CharField): the evaluation choice of the Evaluations.
        description (TextField): the description of the evaluation.
        created_at (DateTimeField): date when the evaluation was created.
        user (ForeignKey): the reference field to the user model.
        order (ForeignKey): the reference field to the order model.
    """

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    class Evaluations(models.TextChoices):
        """evaluations choices
        Args:
            TERRIBLE (tuple[int, str]):
            BAD (tuple[int, str]):
            OK (tuple[int, str]):
            GOOD (tuple[int, str]):
            GREAT (tuple[int, str]):
        """
        TERRIBLE = 1, _("Terrible")
        BAD = 2, _("Bad")
        OK = 3, _("Ok")
        GOOD = 4, _("Good")
        GREAT = 5, _("Great")

    evaluation = models.CharField(
        "Avaliação",
        max_length=1,
        choices=Evaluations,
    )
    description = models.TextField(
        'Descrição',
        max_length=255,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        "Criada em",
        auto_now_add=True,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name="Usuário",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        verbose_name='Pedido'
    )

    def __str__(self) -> str:
        """returns the representation like 'user - order | evaluation'"""
        return f'{self.user} - {self.order} | {self.evaluation}'
