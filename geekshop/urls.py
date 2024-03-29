"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings
from mainapp import views

urlpatterns = [
    path('admin_default', admin.site.urls),    # Стандартная админка
    path('admin/', include('adminapp.urls', namespace='adminapp')),
    path('', views.index, name='index'),
    # path('products/', views.products, name='products'),
    path('products/', include('mainapp.urls', namespace='products')),

    path('auth/', include('authapp.urls', namespace='authapp')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('contact/', views.contact, name='contact'),
    path('orders/', include('ordersapp.urls', namespace='orders')),

    path('', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    # Это для подключение Тол Бара
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

    # Это для того чтоб подключение Статики было только на ЛоКале
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



