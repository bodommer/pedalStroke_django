from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Season)
admin.site.register(Race)
admin.site.register(Plan)