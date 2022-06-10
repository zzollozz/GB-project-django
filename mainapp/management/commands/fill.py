from django.core.management.base import BaseCommand
from mainapp.models import Category, Product
from django.conf import settings
from authapp.models import ShopUser
import json

class Command(BaseCommand):

    @staticmethod
    def _load_data_from_file(file_name):
        with open(f"{settings.BASE_DIR}/mainapp/json/{file_name}.json") as file:
            return json.load(file)

    def handle(self, *args, **options):
        Category.objects.all().delete()
        categories = self._load_data_from_file('categories')

        categories_batch = []
        for cat in categories:
            categories_batch.append(
                Category(
                    name=cat.get('name'),
                    description=cat.get('description')
                )
            )
        Category.objects.bulk_create(categories_batch)  # Вставка списка в базу

        Product.objects.all().delete()
        products_list = self._load_data_from_file('products')

        for product in products_list:
            _cat = Category.objects.get(name=product.get('category'))
            product['category'] = _cat

            Product.objects.create(**product)



        shop_user =  ShopUser.objects.create_superuser(username='django', email='django@bg.local', age=33)
        shop_user.set_password('geekbrains')
        shop_user.save()

