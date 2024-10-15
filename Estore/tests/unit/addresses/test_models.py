import pytest
from django.core.exceptions import ValidationError

from addresses.models import Address, HasAddress


def test_address_str_method():
    """test the __str__ return"""
    addrss = Address(
        street='street',
        state='ST',
        city='city',
        postal_code='12345687890',  # TODO: alter on create validation
        country='CO',
    )
    expected = f"{addrss.street}, {addrss.city} - {addrss.state} / {addrss.country} | {addrss.postal_code}"
    assert str(addrss) == expected


def test_has_address_str_method(admin_user, store, address):
    """test the __str__ return"""
    addrss = HasAddress(
        number='302A',
        complement='',
        user=admin_user,
        store=store,
        address=address
    )
    expected = f"{addrss.number}, {addrss.address}"
    assert str(addrss) == expected


def test_has_address_chk_has_address_fks_not_given_together_constraint_success(
    admin_user, store, address
):
    """test the model chk_has_address_fks_not_given_together constraint success cases"""
    addrss = HasAddress(
        number='302A',
        complement='',
        user=admin_user,
        store=store,
        address=address
    )
    try:
        # both given
        addrss.validate_constraints()
        
    except ValidationError:
        pytest.fail('ValidationError raised')
    
    try:
        # only user given
        addrss.store = None
        addrss.validate_constraints()

    except ValidationError:
        pytest.fail('ValidationError raised')
    
    try:
        # only store given
        addrss.store = store
        addrss.user = admin_user
        addrss.validate_constraints()

    except ValidationError:
        pytest.fail('ValidationError raised')


def test_has_address_chk_has_address_fks_not_given_together_constraint_fail(address):
    """test the model chk_has_address_fks_not_given_together constraint fail 
    when no fks are given.
    """
    addrss = HasAddress(
        number='302A',
        complement='',
        address=address
    )
    with pytest.raises(ValidationError) as e:
        # no one given
        addrss.validate_constraints()
