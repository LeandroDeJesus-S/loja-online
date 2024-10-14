from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from evaluations.models import Evaluation
from products.models import ProductVariation
from utils.support.messages import MediaFileMessages, GenericMessages
from utils.support.validators import FileSizeValidator


class MediaFile(models.Model):
    """model to store files related to the evaluations and
    product variations.

    Args:
        file (FileField): a file of the respective model (`Evaluation` or `ProductVariation`).
        evaluation (ForeignKey): references to the `Evaluation` model.
        product_variation (ForeignKey): references to the ProductVariation model.
    """

    class Meta:
        verbose_name = "Arquivo de mídia"
        verbose_name_plural = "Arquivos de mídia"

    _AVAILABLE_EXTENSIONS = [
        "PNG",
        "JPEG",
        "JPG",
        "WEBP",
        "MP4",
        "AVI",
        "WEBM",
    ]
    _MAX_FILE_SIZE = 4 * 1024**2  # 4MB
    _FILE_HELP_TXT = _(
        "image or video with a maximum of 4MB and in one of "
        f"the following formats: {', '.join(_AVAILABLE_EXTENSIONS)}."
    )

    file = models.FileField(
        "Arquivo",
        null=True,
        validators=[
            FileExtensionValidator(_AVAILABLE_EXTENSIONS),
            FileSizeValidator(
                size=_MAX_FILE_SIZE,
                msg=GenericMessages.FILE_SIZE_EXCEEDED,
            ),
        ],
        help_text=_FILE_HELP_TXT,
    )
    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.DO_NOTHING,
        null=True,
        verbose_name="Avaliação",
    )
    product_variation = models.ForeignKey(
        ProductVariation,
        on_delete=models.DO_NOTHING,
        null=True,
        verbose_name="Produto",
    )

    def __str__(self) -> str:
        """returns the representation like `Avaliação : ... arquivo: ...`
        if the file is to the evaluation, otherwise `Produto: ... arquivo: ...`
        """
        ev = f"Avaliação: {self.evaluation} arquivo: {self.file.name}"
        pdt = f"Produto: {self.product_variation} arquivo: {self.file.name}"
        if self.evaluation is None and self.product_variation is not None:
            return pdt
        elif self.evaluation is not None and self.product_variation is None:
            return ev
        raise Exception(
            "evaluation or product variation cannot be both None or filled, just one of them."
        )

    def clean(self) -> None:
        msg_dict = {}
        self.validate_foreign_keys(msg_dict)

        if msg_dict:
            raise ValidationError(msg_dict, code='invalid')

    def validate_foreign_keys(self, msg_dict: dict):
        """validates if both foreign keys are given together or no one
        of them is given.

        Args:
            msg_dict (dict): dict with error messages for the fields.
        """
        eval_sent = self.evaluation is not None
        pdt_var_sent = self.product_variation is not None

        if eval_sent and pdt_var_sent:
            msg_dict["evaluation"] = msg_dict["product_variation"] = (
                MediaFileMessages.BOTH_FK_SENT
            )

        if not eval_sent and not pdt_var_sent:
            msg_dict["evaluation"] = msg_dict["product_variation"] = (
                MediaFileMessages.NO_FK_SENT
            )
