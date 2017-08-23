from django.db import models
from django.utils import timezone
from plan.model.PlanWeek import PlanWeek

class PlanWeekDay(models.Model):
    dailyHours = models.DecimalField(max_digits=4, decimal_places=2)
    day = models.PositiveIntegerField(0)
    intensity = models.PositiveIntegerField(0)
    workoutType = models.PositiveIntegerField(0)
    week_id = models.ForeignKey(PlanWeek, on_delete=models.CASCADE)
