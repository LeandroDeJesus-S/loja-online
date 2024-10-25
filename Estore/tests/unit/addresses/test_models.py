from addresses.models import Address, UserAddress


def test_address_str_method():
    """test the __str__ return"""
    addrss = Address(
        street='street',
        state='ST',
        city='city',
        postal_code='60714-610',
        country='CO',
    )
    expected = f"{addrss.street}, {addrss.city} - {addrss.state} / {addrss.country} | {addrss.postal_code}"
    assert str(addrss) == expected


def test_user_address_str_method(admin_user, address):
    user_address = UserAddress(
        number='43',
        complement='some extra complement',
        user=admin_user,
        address=address,
    )
    assert str(user_address) == f"{user_address.number}, {user_address.complement}"
