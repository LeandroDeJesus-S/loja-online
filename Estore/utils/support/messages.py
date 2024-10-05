class GenericMessages:
    """class to store generic message constants"""
    INVALID_LEN = '{field} deve ter de {min_len} a {max_len} caracteres.'
    INVALID_MIN_LENGTH = '{field} deve ter no mínimo {size} caracteres.'
    INVALID_MAX_LENGTH = '{field} deve ter no máximo {size} caracteres.'


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
