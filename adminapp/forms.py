from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from django import forms

from mainapp.models import Product, Category


class UserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'
            filed.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ('is_active',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for filed_name, filed in self.fields.items():
    #         filed.widget.attrs['class'] = 'form-control'
    #         filed.help_text = ''


