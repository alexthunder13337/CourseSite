from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from landpage.models import LandpageContactMessage


class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = LandpageContactMessage
        fields = ['name','email', 'phone', 'message']
        labels = {
        }
        widgets = {
            'name': TextInput(attrs={'class': u'form-control','placeholder': u'Введите Ваше полное имя'}),
            'email': EmailInput(attrs={'class': u'form-control','placeholder': u'Введите Ваш Email'}),
            'phone': TextInput(attrs={'class': u'form-control','placeholder': u'Введите Ваш телефон'}),
            'comment': Textarea(attrs={'class': u'form-control','placeholder': u'Введите Ваше сообщение'}),
    }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', None)
        
        # clean phone by removing all non-numerals
        phone = ''.join(x for x in phone if x.isdigit())
        
        ph_length = str(phone)
        min_length = 10
        max_length = 13
        if len(ph_length) < min_length:
            raise ValidationError('Длина телефонного номера минимум 10 цифр')
        if len(ph_length) > max_length:
            raise ValidationError('Телефон не может быть длинне 13 цифр')
        return phone


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Введите Ваш Email'}),
    )
    captcha = CaptchaField()

