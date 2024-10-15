from django.db import models
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
        constraints = [
            models.CheckConstraint(
                condition=models.Q(evaluation__isnull=True, product_variation__isnull=False)|  # type: ignore
                      models.Q(evaluation__isnull=False, product_variation__isnull=True)&
                      ~models.Q(evaluation__isnull=True, product_variation__isnull=True),
                name='chk_mediafile_fks_not_given_together',
                violation_error_message=MediaFileMessages.INVALID_FK_SENT
            )
        ]

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
        
        raise Exception(MediaFileMessages.INVALID_FK_SENT)
