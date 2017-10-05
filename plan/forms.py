from django import forms
from django.utils import timezone 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .model import Profile, Season, Race, Plan
from datetime import date, time

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(label='Password',  max_length=32)

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class NewSeasonForm(forms.Form):
    year = forms.IntegerField(label='Year', min_value=date.today().year, max_value=date.today().year+40)
    
    class Meta:
        model = Season
        fields = ('year')

class NewRaceForm(forms.Form):
    DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')
    name = forms.CharField(label='Race name', max_length=50)
    date = forms.DateField(label='Race day', input_formats=DATE_INPUT_FORMATS)
    priority = forms.IntegerField(label='Priority', max_value=3, min_value=1)
    time = forms.TimeField(label='Expected duration')
    
    class Meta:
        model = Race
        fields = ('name', 'date', 'priority', 'time')

    
class NewPlanForm(forms.Form):
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
    
    class Meta:
        model = Plan
        fields = ('name', 'planStart', 'planEnd', 'annualHours', 'typeOfPlan')
    
class EditProfileForm(forms.Form):
    SKILL_CHOICES = (
        ('Endurance', 'Endurance'),
        ('Force', 'Force'),
        ('Speed Skills', 'Speed Skills'),
        ('Endurance Force', 'Endurance Force'),
        ('Anaerobic Endurance', 'Anaerobic Endurance'),
        ('Maximum Power', 'Maximum Power')
    )

    cp60 = forms.IntegerField(label='CP60 (W)')
    maxHR = forms.IntegerField(label='Maximum Heart Rate (bpm)')
    age = forms.IntegerField(label='Age')
    yearsOfExperience = forms.IntegerField(label='Years of Experience')
    strong1 = forms.ChoiceField(label='Strongest skill',
                                choices=SKILL_CHOICES)
    strong2 = forms.ChoiceField(label='Second strongest skill', 
                                choices=SKILL_CHOICES)
    weak1 = forms.ChoiceField(label='Weakest skills', 
                                choices=SKILL_CHOICES)
    weak2 = forms.ChoiceField(label='Second weakest skill',
                               choices=SKILL_CHOICES)
    
class EditRaceForm(forms.Form):
    PRIORITY = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    )
    
    DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')
    
    name = forms.CharField(label='Race Name', max_length=80)
    date = forms.DateField(label='Race Date', input_formats=DATE_INPUT_FORMATS)
    priority = forms.ChoiceField(label='Priority',
                                choices=PRIORITY)
    time = forms.TimeField(label='Expected duration')
    
    class Meta:
        model = Race
        fields = ('name', 'date', 'priority', 'time')
        
class DeleteSeasonForm(forms.Form):
    pass

class DeleteRaceForm(forms.Form):
    pass

class DeletePlanForm(forms.Form):
    pass