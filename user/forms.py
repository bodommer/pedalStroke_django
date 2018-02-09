from django import forms

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