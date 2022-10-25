import paginate as paginate
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from basketapp.models import Basket
from mainapp.models import Product, Category
from mainapp.services import get_basket, get_hot_product, get_same_products, get_links_menu, get_products, get_product

from django.template.loader import render_to_string
from django.http import JsonResponse

def index(request):
    context = {
        'products': get_products()[:4],
        # 'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context)
# @cache_page(3600) # Кеширование более высокого уровня (Вся страница)
def products(request, pk=None):
    links_menu = get_links_menu()
    if pk is not None:
        if pk == 0:
            products_list = get_products()
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_object_or_404(Category, pk=pk)
            products_list = get_products()

        page = request.GET.get('page')
        paginator = Paginator(products_list, 2)
        try:
            paginated_products = paginator.page(page)
        except PageNotAnInteger:
            paginated_products = paginator.page(1)
        except EmptyPage:
            paginated_products = paginator.page(paginator.num_pages)


        context = {
            'links_menu': links_menu,
            'products': paginated_products,
            'category': category_item,
            # 'basket': get_basket(request.user)
        }
        return render(request, 'mainapp/products_list.html', context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'links_menu': links_menu,
        # 'basket': get_basket(request.user),
        'hot_product': hot_product,
        'same_products': same_products
    }
    return render(request, 'mainapp/products.html', context)

def products_ajax(request, pk=None):
    links_menu = get_links_menu()
    if pk is not None:
        if pk == 0:
            products_list = get_products()
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_object_or_404(Category, pk=pk)
            products_list = get_products()

        page = request.GET.get('page')
        paginator = Paginator(products_list, 2)
        try:
            paginated_products = paginator.page(page)
        except PageNotAnInteger:
            paginated_products = paginator.page(1)
        except EmptyPage:
            paginated_products = paginator.page(paginator.num_pages)

        content = {
            'links_menu': links_menu,
            'category': category_item,
            'products': paginated_products,
        }
        result = render_to_string('mainapp/includes/inc_products_list_content.html',
                                  context=content,
                                  request=request)
        return JsonResponse({'result': result})

def product(request, pk):
    product_item = get_product(pk)
    context = {
        'product': product_item,
        # 'basket': get_basket(request.user),
        'links_menu': get_links_menu(),
    }
    return render(request, 'mainapp/product.html', context)

def contact(request):
    context = {
        # 'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context)
