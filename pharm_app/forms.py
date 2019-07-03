from django.forms import ModelForm
from pharm_app.models import pharma, activation_info, medicine_composition
from django import forms

class pharma_signup_form(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = pharma
        fields = ['organization_name', 'location_address_1', 'location_address_2', 'email', 'mobile', 'password']

class pharma_signin_form(forms.Form):
    email = forms.CharField(widget = forms.EmailInput())
    password = forms.CharField(widget = forms.PasswordInput())

class activation_form(ModelForm):
    class Meta:
        model = activation_info
        fields = ['pin']

class medicine_form(forms.Form):
    medicine = forms.CharField(max_length = 300)
    file = forms.FileField()

class composition_form(ModelForm):
    class Meta:
        model = medicine_composition
        fields = ['composition', 'weightage']

class user_form(forms.Form):
    medicine = forms.CharField(max_length = 200)
