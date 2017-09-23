from django.db import models
from datetime import time, tzinfo
from django.utils import timezone
from plan.model.Season import Season

class Race(models.Model):
    PRIORITY = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    )

    date = models.DateField(default=timezone.now())
    name = models.CharField(max_length=80, default="")
    priority = models.PositiveIntegerField('Priority', choices=PRIORITY, default=PRIORITY[0])
    time = models.TimeField(time(0,0,0))
    parent_season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.name, self.date.year)

    def save_data(self, data, season_id):
        self.date = data['date']
        self.name = data['name']
        self.priority = data['priority']
        self.time = data['time']
        self.parent_season = Season(season_id)