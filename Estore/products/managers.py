from django.db.models import Manager


class ProductManager(Manager):
    def available(self):
        return self.filter(variation_option_data__stock__gte=1).distinct()
