from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse
from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import F

@login_required
def basket_list(request):
    context = {
        'basket_items': Basket.objects.filter(user=request.user)
    }
    return render(request, 'basketapp/list.html', context)
    # return render(request, 'basketapp/includes/inc_basket_list.html', context)

@login_required
def basket_add(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(product=product_item, user=request.user).first()
    if not basket_item:
        basket_item = Basket(product=product_item, user=request.user)
    basket_item.quantity += 1
    basket_item.save()
    
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product_item', args=[pk]))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, pk):
    Basket.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_edit(request, pk, quantity):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.quantity = quantity
    basket_item.save()

    context = {
        'basket_items': Basket.objects.filter(user=request.user)
    }
    # return render(request,'basketapp/includes/inc_basket_list.html', context)
    rendered_template = render_to_string('basketapp/includes/inc_basket_list.html', context)
    return JsonResponse({'result': rendered_template})
