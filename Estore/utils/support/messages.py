class GenericMessages:
    """class to store generic message constants"""
    INVALID_LEN = '{field} deve ter de {min_len} a {max_len} caracteres.'
    INVALID_MIN_LENGTH = '{field} deve ter no mínimo {size} caracteres.'
    INVALID_MAX_LENGTH = '{field} deve ter no máximo {size} caracteres.'


class AddressMessages:
    """messages related to addresses"""
    INVALID_COUNTRY = 'O país fornecido é inválido'
    INVALID_STATE = 'Estado inválido.'


class StoreMessages:
    """class with message constants related to the Store entity"""
    INVALID_CNPJ = 'CPJ inválido.'
    INVALID_NAME = 'O nome da loja é inválido'
    INVALID_NAME_LEN = 'O nome precisa ter de {minlen} a {maxlen} caracteres.'


class ProductMessages:
    """messages related to the product entity"""
    INVALID_NAME = 'Nome inválido.'
    INVALID_PRICE = 'Preço inválido.'


class CategoryMessages:
    """messages related to the products category"""
    INVALID_NAME = 'O nome da categoria é inválido.'


class OrderMessages:
    """messages related to the orders"""
    INVALID_ORDER_STATUS_NAME = 'O status é inválido.'
    INVALID_STRIPE_PAYMENT_ID = 'O id do pagamento é inválido.'
    INVALID_STRIPE_PAYMENT_METHOD = 'O id do método de pagamento é inválido.'
