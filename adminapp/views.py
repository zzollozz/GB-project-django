# import success as success
from django.shortcuts import render, get_object_or_404

from adminapp.forms import UserAdminEditForm, ProductEditForm, CategoryEditForm
from authapp.models import ShopUser
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from mainapp.models import Category, Product
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.db.models import F


class AccessMixim(UserPassesTestMixin):
    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)
    def test_func(self):
        return self.request.user.is_authenticated

def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    return None


class UserListView(AccessMixim, ListView):
    model = ShopUser
    template_name = 'adminapp/user_list.html'
    paginate_by = 2


class UserUpdateView(AccessMixim, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = UserAdminEditForm
    # success_url = reverse_lazy('adminapp:user_read')

    def get_success_url(self):
        return reverse('adminapp:user_update', args=[self.kwargs.get('pk')])



@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user_item = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_item.is_active = False
        user_item.save()
        return HttpResponseRedirect(reverse('adminapp:user_read'))
    context = {
        'object': user_item
    }
    return render(request, 'adminapp/user_delete_confirm.html', context)


class CategoryCreateView(AccessMixim, CreateView):
    model = Product
    form_class = CategoryEditForm
    # fields = ('name', 'description')
    success_url = reverse_lazy('adminapp:category_read')
    template_name = 'adminapp/category_create.html'


@user_passes_test(lambda u: u.is_superuser)
def category_read(request):
    context = {
        'objects_list': Category.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/category_list.html', context)

class CategoryUpdateView(AccessMixim, UpdateView):
    model = Category
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:category_read')
    # fields = '__all__'
    form_class = CategoryEditForm

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    return None

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'adminapp/category_delete.html'
    context_object_name = 'product_to_delete'
    success_url = reverse_lazy('adminapp:category_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request):
    return None


# @user_passes_test(lambda u: u.is_superuser)
# def products_read(request, pk):
#     category_item = get_object_or_404(Category, pk=pk)
#     products_list = Product.objects.filter(category_id=pk)
#     context = {
#         'objects_list': products_list,
#         'category': category_item
#     }
#     return render(request, 'adminapp/products_list.html', context)


# class ProductListView(ListView):
#     model = Product
#     template_name = 'adminapp/products_list.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(*args, **kwargs)
#         context_data['category'] = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#         return context_data
#
#     def get_queryset(self):
#         return super().get_queryset().filter(category_id=self.kwargs.get('pk'))

class CategoryDetailView(AccessMixim, DetailView):
    model = Category
    template_name = 'adminapp/products_list.html'


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    category_item = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_item = product_form.save()
            return HttpResponseRedirect(reverse('adminapp:products_read', args=[product_item.category.pk]))
    else:
        product_form = ProductEditForm()
    context = {
        'form': product_form
    }
    return render(request, 'adminapp/product_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    return None



class ProductDeleteView(AccessMixim, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete_confirm.html'

    def get_success_url(self):
        category_pk = self.get_object().category_id
        return reverse('adminapp:products_read', args=[category_pk])

    def delete(self, *args, **kwargs):
        self.object = self.get.object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductDetailView(AccessMixim, DetailView):
    model = Product
    template_name = 'adminapp/product_info.html'

@receiver(pre_save, sender=Category)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
