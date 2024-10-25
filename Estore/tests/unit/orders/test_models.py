from orders.models import Order, OrderProductVariation


def test_order_str_method(admin_user):
    """test the __str__method return"""
    order = Order(
        total_items=1,
        total_amount=10,
        status=Order.PAID,
        user=admin_user,
    )
    tot_items = order.total_items
    amount = order.total_amount
    status = order.status
    assert str(order) == f'{tot_items}, {amount} | {status}'


def test_order_product_variation_str_method(pending_order, product_variation):
    """test the return of the __str__ method"""
    opv = OrderProductVariation(
        order=pending_order,
        product_variation=product_variation,
        qtd=1
    )
    assert str(opv) == f'{opv.order}, {opv.product_variation} | {opv.qtd}'
