from django import forms
from django.utils import timezone

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(label='Password',  max_length=32)
    
class SignupForm(forms.Form):
    SKILL_CHOICES = (
        ('endurance', 'Endurance'),
        ('force', 'Force'),
        ('speedSkills', 'Speed Skills'),
        ('eForce', 'Endurance Force'),
        ('aEndurance', 'Anaerobic Endurance'),
        ('maxPower', 'Maximum Power')
    )
        
    username = forms.CharField(label='Username', max_length=32)
    email = forms.CharField(label='E-mail', max_length=100)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    age = forms.IntegerField(label='Age', max_value=99, min_value=8)
    cp60 = forms.IntegerField(label='CP60', max_value=500, min_value=40)
    maxHR = forms.IntegerField(label='Maximum heart rate', max_value=225, min_value=120)
    yearsOfExperience = forms.IntegerField(label='Years of experience', min_value=0, max_value=99)
    strong1 = forms.ChoiceField(SKILL_CHOICES)
    strong2 = forms.ChoiceField(SKILL_CHOICES)
    weak1 = forms.ChoiceField(SKILL_CHOICES)
    weak2 = forms.ChoiceField(SKILL_CHOICES)

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