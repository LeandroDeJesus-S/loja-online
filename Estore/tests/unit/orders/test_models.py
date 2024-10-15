from orders.models import Order, OrderStatus


def test_order_status_str_method():
    """test the __str__method return"""
    order_status = OrderStatus(name='ok')
    assert str(order_status) == 'ok'


def test_order_str_method(processing_order_status, admin_user, product_variation):
    """test the __str__method return"""
    order = Order(
        qtd=1,
        status=processing_order_status,
        user=admin_user,
        product_variation=product_variation
    )
    username = admin_user.username
    var = str(product_variation)
    status = processing_order_status.name
    qtd = order.qtd
    assert str(order) == f'{username} | {var}, {qtd} - {status}'


def test_order_value_return(processing_order_status, admin_user, product_variation):
    """test if the order_value method return the correct value as int 
    and decimal
    """
    order = Order(
        qtd=2,
        status=processing_order_status,
        user=admin_user,
        product_variation=product_variation
    )
    expected_decimal = order.qtd * product_variation.price
    expected_int = int(expected_decimal * 100)
    
    result_decimal = order.order_value()
    result_int = order.order_value(as_int=True)

    assert result_decimal == expected_decimal
    assert result_int == expected_int
