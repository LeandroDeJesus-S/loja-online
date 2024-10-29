from django.template import Library
from functools import reduce

register = Library()


@register.filter
def get_cart_quantity(cart):
    """returns the number of the total item in the cart"""
    if not cart:
        return ''
    
    result = reduce(
        lambda initial, item: initial + item[1]['qtd'],
        cart.items(),
        0,
    )
    return result


@register.filter
def get_cart_total_amount(products):
    """return the total amount of the cart products"""
    if not products:
        return ''
    return sum([o['amount'] for o in products])
