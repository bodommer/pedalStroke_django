from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views import generic
from plan.model.User import User
from plan.model.Season import Season
from plan.model.Race import Race
from plan.model.Plan import Plan
from plan.model.PlanWeek import PlanWeek

from .forms import *
from django.views.decorators.csrf import csrf_protect

class IndexView(generic.View):

    def index(request):
        return render(request, 'plan/index.html')
    
    def about(request):
        return render(request, 'plan/about.html')
    #===================================================================
    # try:
    #     user_list = User.objects.order_by('-age')
    # except:
    #     raise Http404("No users found")
    # context = {'user_list': user_list}
    # return render(request, 'plan/index.html', context)
    #===================================================================
    # a django shortcut, args: request, template location, context data

#===============================================================================
# class UserView(generic.ListView):
#     template_name = 'plan/user.html'
#     context_object_name = 'season'
#     season = get_list_or_404(fk=user_id)
#     
#     def get_queryset(self):
#         return Season.get_all_objects_for_this_type()
#===============================================================================

class UserView(generic.View):
    def user(request, user_id):
        seasons = get_list_or_404(Season, fk=user_id)
        return render(request, 'plan/')

    def home(request, user_id):
        user = get_object_or_404(User, pk=user_id)
        seasons = get_list_or_404(Season, user_id=user_id)
        return render(request, 'plan/home.html', {'user': user, 'seasons': seasons})
    
    def login(request):
        csrf_protect
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user_list = User.objects.order_by('-age')
                user_id = get_object_or_404(User, name=data['username']).id
                string = '/plan/' + str(user_id) + '/'
                return HttpResponseRedirect(string)
        else:
            form = LoginForm()
        return render(request, 'plan/login.html', {'form': form})
    
    def sign_up(request):
        csrf_protect
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                string = '/plan/'
                return HttpResponseRedirect(string)
        else:
            form = SignupForm()
        return render(request, 'plan/sign_up.html', {'form': form})
        #return render(request, 'plan/sign_up.html')

class SeasonView(generic.View):

    def new_season(request, user_id):
        csrf_protect
        if request.method == 'POST':
            form = NewSeason(request.POST)
            if form.is_valid():
                string = '/plan/' + user_id + '/'
                return HttpResponseRedirect(string)
        else:
            form = NewSeason()
        return render(request, 'plan/new_season.html', {'form': form, 'user_id':user_id})
    
    def season(request, user_id, season_id):
        season = get_object_or_404(Season, pk=season_id)
        races = Race.objects.filter(season_id = season_id)
        plans = Plan.objects.filter(season_id=season_id)
        for plan in plans:
            plan.count_load(PlanWeek.objects.filter(plan_id = plan.id).values_list('weeklyHours'))
        return render(request, 'plan/season.html', {'user_id': user_id, 'season': season, 'races': races, 'plans': plans})

class RaceView(generic.View):

    def new_race(request, user_id, season_id):
        csrf_protect
        if request.method == 'POST':
            form = NewRace(request.POST)
            if form.is_valid():
                string = '/plan/' + user_id + '/season/' + season_id + '/'
                return HttpResponseRedirect(string)
        else:
            form = NewRace()
        return render(request, 'plan/new_race.html', {'form': form, 'user_id':user_id, 'season_id': season_id})

class PlanView(generic.View):

    def new_plan(request, user_id, season_id):
        csrf_protect
        if request.method == 'POST':
            form = NewPlan(request.POST)
            if form.is_valid():
                string = '/plan/' + user_id + '/season/' + season_id + '/'
                return HttpResponseRedirect(string)
        else:
            form = NewPlan()
        return render(request, 'plan/new_plan.html', {'form': form, 'user_id':user_id, 'season_id': season_id})
    
    def plan(request, user_id, plan_id):
        plan = get_object_or_404(Plan, pk=plan_id)
        return render(request, 'plan/plan.html', {'plan': plan})



