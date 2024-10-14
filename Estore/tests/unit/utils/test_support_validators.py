import pytest
from django.core.exceptions import ValidationError
from utils.support.validators import FileSizeValidator, validate_cnpj


def test_file_size_validator_success():
    """test success case to the file size validator
    """
    message = 'bad size'
    fake_img_size = 1024
    expected_size = 1024

    class FakeFilefield:
        size = fake_img_size

    try:
        FileSizeValidator(
            size=expected_size, msg=message
        )(FakeFilefield)
    except ValidationError:
        pytest.fail('ValidationError raised.')


def test_file_size_validator_fail():
    """test if raises validation error whe the file is greatest than
    the validation size
    """
    message = 'bad size'
    fake_img_size = 1024
    bad_max_size = 1023

    class FakeFilefield:
        size = fake_img_size

    with pytest.raises(ValidationError) as e:
        FileSizeValidator(
            size=bad_max_size, msg=message
        )(FakeFilefield)

    assert e.value.message == message


@pytest.mark.parametrize(
    'cnpj', ['19.982.055/0001-72', '74473068000124']
)
def test_cnpj_validator_success(cnpj):
    """test the success cases for cnpj validator.

    Args:
        cnpj (str): the cnpj with and without punctuation.
    """
    try:
        validate_cnpj(cnpj)
    except ValidationError:
        pytest.fail('ValidationError raised.')


@pytest.mark.parametrize(
    'cnpj,expected_msg',
    [
        ('19.982.055', "The CNPJ must have 14 chars."),
        ('19.982.055/0001-75', "the CNPJ is invalid."),
        ('74473068000114', "the CNPJ is invalid."),
    ],
)
def test_cnpj_validator_fail(cnpj: str, expected_msg: str):
    """test the fail cases for cnpj validator.

    Args:
        cnpj (str): the cnpj with invalid last digits.
        expected_message (str): the error message expected.
    """
    with pytest.raises(ValidationError) as e:
        validate_cnpj(cnpj)
    
    assert e.value.message == expected_msg
