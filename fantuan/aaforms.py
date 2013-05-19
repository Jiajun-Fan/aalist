from django import forms
from django.contrib.auth.models import User 
from fantuan.models import MyGroup

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class GroupForm(forms.ModelForm):
    class Meta:
        model = MyGroup
        fields = ['name', ]

class OptionForm(forms.Form):
    select = forms.BooleanField(widget=forms.CheckboxInput(), required=False, initial=False) 
    uid = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.FloatField(required=False)
    credit = forms.FloatField(required=False)
    paid = forms.FloatField(initial=0)
    own = forms.FloatField(initial=0)
