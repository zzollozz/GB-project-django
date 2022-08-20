from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from authapp.models import ShopUser, ShopUserProfile
import re
import random, hashlib


class ShopUserLoginForm(AuthenticationForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'password',)

        def __init__(self, *args, **kwargs):
            super().__init__(**args, ** kwargs)
            for file_name, filed in self.fields.items():
                filed.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'password1', 'password2')

        def __init__(self, *args, **kwargs):
            super().__init__(**args, ** kwargs)
            for file_name, filed in self.fields.items():
                filed.widget.attrs['class'] = 'form-control'

    def clean_age(self):
        current_age = self.cleaned_data['age']
        if current_age < 18:
            raise forms.ValidationError("Вы слишком молоды!")
        return current_age

    def save(self):
        user = super(ShopUserRegisterForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class ShopUserEditForm(UserChangeForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'password')

        def __init__(self, *args, **kwargs):
            super().__init__(**args, ** kwargs)
            for filed_name, filed in self.fields.items():
                filed.widget.attrs['class'] = 'form-control'
                filed.help_text = ""
                if filed_name == 'password':
                    filed.widget = forms.HiddenInput()

        def clean_age(self):
            current_age = self.cleaned_data['age']
            if current_age < 18:
                raise forms.ValidationError("Вы слишком молоды!")
            return current_age


        def clean_email(self):
            pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
            email = self.cleaned_data['email']
            if re.match(pattern, email) is not None:
                raise forms.ValidationError("Адресс введен не верно!")
            return email

class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ('tagline', 'aboutMe', 'gender')
    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'