from django import forms
from unittest.util import _MAX_LENGTH

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(label='Password',  max_length=32)