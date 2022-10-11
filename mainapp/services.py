import random

from basketapp.models import Basket
from mainapp.models import Product, Category
from django.shortcuts import get_object_or_404

from django.conf import settings
from django.core.cache import cache

def get_links_menu():
    """ Для кеширования меню """
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = Category.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return Category.objects.filter(is_active=True)

# def get_category(pk):
#     if settings.LOW_CACHE:
#         key = f'category_{pk}'
#         category = cache.get(key)
#         if category is None:
#             category = get_object_or_404(ProductCategory, pk=pk)
#             cache.set(key, category)
#         return category
#     else:
#         return get_object_or_404(ProductCategory, pk=pk)

def get_products():
    """ Для кеширования продуктов """
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')

def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)

def get_basket(user):
    basket_list = []
    if user.is_authenticated:
        basket_list = Basket.objects.filter(user=user)
    return basket_list

def get_hot_product():
    return get_products().order_by('?').first()  # выберается объект с Базы

    # products_list = Product.objects.all()             # Выберается уже через КвериСет а это медленно
    # return random.sample(list(products_list), 1)[0]   # Использовать если небольшое количество


def get_same_products(product):
    return Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]
