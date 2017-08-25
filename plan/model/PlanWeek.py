from django.db import models
from django.utils import timezone
from plan.model.Plan import Plan


class PlanWeek(models.Model):
    aEndurance = models.PositiveSmallIntegerField(0)
    eForce = models.PositiveSmallIntegerField(0)
    endurance = models.PositiveSmallIntegerField(0)
    force = models.PositiveSmallIntegerField(0)
    gym = models.CharField(max_length=10)
    maxPower = models.PositiveSmallIntegerField(0)
    monday = models.DateField()
    period = models.CharField(max_length=25)
    speedSkills = models.PositiveSmallIntegerField(0)
    test = models.PositiveSmallIntegerField(0)
    week = models.PositiveSmallIntegerField(0)
    weeklyHours = models.DecimalField(max_digits=5, decimal_places=1)
    races = models.CharField(max_length=300)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return "Week {}".format(self.week)
