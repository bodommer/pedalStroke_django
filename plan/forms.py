from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(label='Password',  max_length=32)

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class NewSeason(forms.Form):
    year = forms.IntegerField(label='Year', min_value=2017, max_value=2057)

class NewRace(forms.Form):
    DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')
    
    name = forms.CharField(label='Race name', max_length=50)
    date = forms.DateField(label='Race day', input_formats=DATE_INPUT_FORMATS)
    priority = forms.IntegerField(label='Priority', max_value=3, min_value=1)
    time = forms.TimeField(label='Expected duration')
    
class NewPlan(forms.Form):
    PLAN_CHOICES = (
        ('normal', 'Normal'),
        ('reversed', 'Reversed')
    )
    DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')
    HOURS_CHOICES = [('{}'.format(i*50), '{}'.format(i*50)) for i in range(4, 25)]
    
    name = forms.CharField(label='Plan Name', max_length=32)
    planStart = forms.DateField(label='Plan Start', input_formats=DATE_INPUT_FORMATS)
    planEnd = forms.DateField(label='Plan End', input_formats=DATE_INPUT_FORMATS)
    annualHours = forms.ChoiceField(HOURS_CHOICES)
    typeOfPlan = forms.ChoiceField(PLAN_CHOICES)