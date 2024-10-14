from django.utils.translation import gettext_lazy as _


class GenericMessages:
    """class to store generic message constants"""
    INVALID_LEN = '`{field}` must have between `{min_len}` and `{max_len}` characters.'
    INVALID_MIN_LENGTH = '`{field}` must have at least `{size}` characters.'
    INVALID_MAX_LENGTH = '`{field}` must have at most `{size}` characters.'
    FILE_SIZE_EXCEEDED = _('the file size is too big.')


class AddressMessages:
    """messages related to addresses"""
    INVALID_COUNTRY = _('Invalid county.')
    INVALID_STATE = _('Invalid state')


class StoreMessages:
    """class with message constants related to the Store entity"""
    INVALID_CNPJ = _('the CPJ is invalid.')
    INVALID_NAME = _('the store name is invalid')


class ProductMessages:
    """messages related to the product entity"""
    INVALID_NAME = _('the name of the product is invalid.')
    INVALID_PRICE = _('invalid product price.')


class CategoryMessages:
    """messages related to the products category"""
    INVALID_NAME = _('The name of the category is invalid.')


class OrderMessages:
    """messages related to the orders"""
    INVALID_ORDER_STATUS_NAME = _('invalid status.')
    INVALID_STRIPE_PAYMENT_ID = _('Invalid stripe payment id.')
    INVALID_STRIPE_PAYMENT_METHOD_ID = _('The stripe payment method id is invalid.')


class MediaFileMessages:
    """messages to media files domain"""
    BOTH_FK_SENT = _('The file must be for either evaluation or product, not both.')
    NO_FK_SENT = _('The file must be related to a review or product.')
