from django.db import models
from django.utils import timezone
from user.model.Profile import Profile

class Season(models.Model):
    year = models.PositiveIntegerField('Season', default=timezone.now().year)
    parent_user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return "Season {}".format(self.year)
    
    def save_data(self, year, parent_user):
        self.year = year
        self.parent_user = Profile(parent_user)