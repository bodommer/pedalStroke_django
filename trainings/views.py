from django.shortcuts import render

# Create your views here.
from django.views import generic


class TrainingsView(generic.View):

    def index(request):
        return render(request, 'trainings/overview.html')