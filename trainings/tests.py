#from django.test import TestCase
from plan.model.Season import Season
from django.contrib.auth.models import User
from unittest import TestCase
import profile

class TestNewSeason(TestCase):
    def setUp(self):
        self.aaa = "aaa"
        
    def test_newSeason(self):
        bbb = "bbb"
        self.assertNotEqual(self.aaa, bbb)
        
        
if __name__ == '__main__':
    unittest.main()