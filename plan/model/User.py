from django.db import models

class User(models.Model):
    SKILL_CHOICES = (
        ('endurance', 'Endurance'),
        ('force', 'Force'),
        ('speedSkills', 'Speed Skills'),
        ('eForce', 'Endurance Force'),
        ('aEndurance', 'Anaerobic Endurance'),
        ('maxPower', 'Maximum Power')
    )

    name = models.CharField(max_length=50, unique=True, default="")
    cp60 = models.PositiveIntegerField('CP60 (W)', default=100)
    maxHR = models.PositiveIntegerField('Maximum Heart Rate (bpm)', default=180)
    age = models.PositiveIntegerField('Age', default=18)
    yearsOfExperience = models.PositiveIntegerField('Years of Experience', default=0)
    strong1 = models.CharField('Strongest skill', max_length=30,
                                choices=SKILL_CHOICES, default='endurance')
    strong2 = models.CharField('Second strongest skill', max_length=30,
                                choices=SKILL_CHOICES, default='endurance')
    weak1 = models.CharField('Weakest skills', max_length=30,
                                choices=SKILL_CHOICES, default='endurance')
    weak2 = models.CharField('Second weakest skill', max_length=30,
                                choices=SKILL_CHOICES, default='endurance')

    def __str__(self):
        return "{} ({})".format(self.name, self.age)
