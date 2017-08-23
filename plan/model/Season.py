from django.db import models
from django.utils import timezone
from plan.model.User import User

class Season(models.Model):
    year = models.PositiveIntegerField('Season', default=timezone.now().year)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Season {}".format(self.year)
