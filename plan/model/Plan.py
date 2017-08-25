from django.db import models
from django.utils import timezone
from datetime import date, timedelta
from plan.model.Season import Season

class Plan(models.Model):
    PLAN_CHOICES = (
        ('normal', 'Normal'),
        ('reversed', 'Reversed')
    )

    start = date.today()
    end = start + timedelta(weeks=52)

    annualHours = models.PositiveIntegerField('Annual hours', default=200)
    typeOfPlan = models.CharField('Type of Plan', max_length=20,
                                  choices=PLAN_CHOICES, default='normal')
    planStart = models.DateField('Start of Plan', default=start)
    planEnd = models.DateField('End of Plan', default=end)
    season_id = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-hour plan for {}".format(self.annualHours, self.season_id)

    def count_load(self, weekset):
        load = 0
        print(weekset)
        for a in weekset: 
            load += a
        self.load = load