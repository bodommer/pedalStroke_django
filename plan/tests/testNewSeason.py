from django.test import TestCase
from plan.model.Season import Season

class testNewSeason(TestCase):
    def setUp(self):
        defaultSeason = Season(year=2018)
        
    def newSeason(self):
        season = Season(year=2018)
        self.assertIs(defaultSeason, season, "The season are not equal")