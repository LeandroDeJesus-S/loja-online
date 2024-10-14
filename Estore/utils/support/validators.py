from typing import Any
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator:
    """validate if the file size is less or equal than the given `size` param"""

    def __init__(self, size: int, msg: str) -> None:
        """
        Args:
            size (int): the expected size in bytes format.
            msg (str): the error message.
        """
        self.size = size
        self.msg = msg

    def __call__(self, filefield) -> Any:
        if filefield.size > self.size:
            raise ValidationError(
                self.msg, code="invalid", params={"filesize": filefield.size}
            )

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, FileSizeValidator) and 
            value.__dict__ == self.__dict__
        )


def validate_cnpj(cnpj):
    """makes the calculus to validate the CNPJ."""
    cnpj = re.sub(r"\D", "", cnpj)

    if len(cnpj) != 14:
        raise ValidationError(
            _("The CNPJ must have 14 chars."),
            code="invalid",
            params={"chars": len(cnpj)},
        )

    def calc_digit(cnpj, first=True):
        prods = list(range(6 if first else 5, 10)) + list(range(2, 10))
        digits = list(map(lambda x: int(x[0]) * x[1], zip(cnpj, prods)))
        digit = sum(digits) % 11
        if digit > 9:
            digit = 0
        return digit

    base, real_last_digits = cnpj[:12], cnpj[12:]
    d13 = calc_digit(base)
    d14 = calc_digit(base + str(d13), first=False)

    if f"{d13}{d14}" != real_last_digits:
        raise ValidationError(_("the CNPJ is invalid."), code="invalid")
