from django.urls import path

from basketapp.views import basket_list, basket_add, basket_remove

app_name = 'basket'

urlpatterns = [
    path('', basket_list, name='List'),
    path('add/<pk>/', basket_add, name='add'),
    path('remove/<pk>/', basket_remove, name='remove'),
]
