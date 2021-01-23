from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='Имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Введите имя'}),
        required=True,
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Введите фамилию'}),
        required=True,
    )
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={
            'autocorrect':'off',
            'autocapitalize':'none',
            'class':'form-control',
            'placeholder':'Введите Email'
        }),
        required=True,
    )
    password = forms.CharField(
        label='Пароль',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder':'Ввведите пароль'
        }),
        required=True,
    )
    password_repeated = forms.CharField(
        label='Повтор пароля',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder':'Введите пароль ещё раз'
        }),
        required=True,
    )
    captcha = CaptchaField()

    # Functions
    #------------
    def clean_email(self):
        email = self.cleaned_data['email']
        if email is not None and email is not '':
            try:
                User.objects.get(email=email)
                raise forms.ValidationError("Данный e-mail уже зарегестрирован на портале.")
            except User.DoesNotExist:
                return email
        else:
            raise forms.ValidationError("Поле не  может быть пустым")


    def clean_password_repeated(self):
        password = self.cleaned_data['password'] # cleaned_data dictionary has the
        # the valid fields
        password_repeated = self.cleaned_data['password_repeated']
        if password != password_repeated:
            raise forms.ValidationError("Пароли не совпадают.")
        return password_repeated


# Captcha Setup:
# http://django-simple-captcha.readthedocs.org/en/latest/usage.html#installation