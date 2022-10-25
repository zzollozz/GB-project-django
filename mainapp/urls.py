from django.urls import path
from mainapp.views import products, product, products_ajax
from django.views.decorators.cache import cache_page

app_name = 'products'

urlpatterns = [
    path('', products, name='products_hot_product'),
    path('<int:pk>/', products, name='product_list'),
    path('product/<int:pk>/', product, name='product_item'),

    path('<int:pk>/ajax/', products_ajax)
]


