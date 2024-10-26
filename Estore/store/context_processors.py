from .models import Store


def store(request) -> dict[str, Store | None]:
    """returns the first instance of the model Store with the
    base info data of the store
    """
    return {'store': Store.objects.first()}
