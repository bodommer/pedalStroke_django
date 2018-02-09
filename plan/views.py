from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.loader import *
from django.views import generic
import base64
from datetime import time, tzinfo
from django.utils import timezone
from user.model.Profile import Profile
from plan.model.Season import Season
from plan.model.Race import Race
from plan.model.Plan import Plan, PlanWeek

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from plan.forms import NewSeasonForm, NewRaceForm, NewPlanForm, EditRaceForm, DeleteSeasonForm, DeleteRaceForm, DeletePlanForm
from plan.tokens import account_activation_token
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import logout_then_login
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.forms.models import model_to_dict
from datetime import date, datetime
from django.db import connection

class IndexView(generic.View):

    def index(request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/plan/' + str(request.user.id) + '/')
        return render(request, 'home/index.html')
    
    def about(request):
        if request.user.is_authenticated:
            return render(request, 'home/about_logged.html')
        return render(request, 'home/about.html')

class UserView(generic.View):
    def user(request, user_id):
        seasons = get_list_or_404(Season, fk=user_id)
        return render(request, 'plan/')

    def home(request, user_id):
        if request.user.is_authenticated:
            if str(request.user.id) == user_id:
                seasons = Season.objects.filter(parent_user = request.user.id).order_by('year')
                return render(request, 'plan/plan_home.html', {'user': request.user, 'seasons': seasons})
        return render(request, 'default_sites/unauthorised_access.html')

class SeasonView(generic.View):

    def new_season(request, user_id):
        if request.user.is_authenticated():
            if str(request.user.id) == user_id:
                csrf_protect
                if request.method == 'POST':
                    form = NewSeasonForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        if len(Season.objects.filter(parent_user=user_id, year=data['year'])) == 0:
                            season = Season()
                            season.save_data(year=data['year'], parent_user=user_id)
                            season.save()
                            string = '/plan/' + user_id + '/'
                            return HttpResponseRedirect(string)
                        else:
                            messages = ('You have already created the ' + str(data['year']) + ' season',)
                            form = NewSeasonForm(initial={'year': data['year']})
                            return render(request, 'plan/new_season.html', {'form': form, 'messages': messages, 'user_id':user_id})
                else:
                    form = NewSeasonForm(initial={'year': date.today().year})
                return render(request, 'plan/new_season.html', {'form': form, 'user_id':user_id})
            messages = ('You do not have access to this site!',)
            return render(request, 'default_sites/message_site_logged.html', {'messages': messages})
        messages = ('You are not authorised to access this site!',)
        return render(request, 'default_sites/message_site.html', {'messages': messages})

    def season(request, user_id, season_id):
        csrf_protect
            #if submit value is 'delete-races' - delete selection of the races
            #if submit value is 'delete-plans' - delete selection of the plans
        season = get_object_or_404(Season, pk=season_id)
        races = Race.objects.filter(parent_season=season_id)
        for race in races:
            race.time = '{:d}:{:02d}:{:02d}'.format(race.time.hour, race.time.minute, race.time.second)
        plans = Plan.objects.filter(parent_season=season_id)
        #for plan in plans:
        #    plan.count_load(PlanWeek.objects.filter(plan_id = plan.id).values_list('weeklyHours'))
        return render(request, 'plan/season.html', {'user_id': user_id, 'season': season, 'races': races, 'plans': plans})
    
    def seasonDelete(request, user_id, season_id):
        if request.user.is_authenticated:
            season = False
            if str(request.user.id) == str(user_id):
                csrf_protect
                if request.method == 'POST':
                    season = Season.objects.filter(pk=season_id, parent_user=user_id)
                    if season:
                        season.delete()
        return redirect('plan:user', user_id)

class RaceView(generic.View):

    def new_race(request, user_id, season_id):
        if request.user.is_authenticated():
            if str(request.user.id) == user_id:
                csrf_protect
                if request.method == 'POST':
                    form = NewRaceForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        race = Race()
                        race.save_data(data, season_id)
                        race.save()
                        string = '/plan/' + user_id + '/season/' + season_id + '/'
                        return HttpResponseRedirect(string)
                else:
                    today = date.today()
                    form = NewRaceForm(initial={'priority': 1, 'date': '{}-{:02d}-{}'.format(today.day, today.month, today.year), 'time': '0:00:00'})
                return render(request, 'plan/new_race.html', {'form': form, 'user_id':user_id, 'season_id': season_id})
            messages = ('You do not have access to this site!',)
            return render(request, 'default_sites/message_site_logged.html', {'messages': messages})
        messages = ('You are not authorised to access this site!',)
        return render(request, 'default_sites/message_site.html', {'messages': messages})
    
    def race(request, user_id, season_id, race_id):
        if request.user.is_authenticated():
            if str(request.user.id) == user_id:
                csrf_protect
                race = Race.objects.filter(id=race_id)[0]
                race.time = '{:d}:{:02d}:{:02d}'.format(race.time.hour, race.time.minute, race.time.second)
                return render(request, 'plan/race.html', {'race': race, 'season_id': season_id})
            messages = ('You do not have access to this site!',)
            return render(request, 'default_sites/message_site_logged.html', {'messages': messages})
        messages = ('You are not authorised to access this site!',)
        return render(request, 'default_sites/message_site.html', {'messages': messages})
    
    def raceEdit(request, user_id, season_id, race_id):
        if request.user.is_authenticated:
            if str(request.user.id) == str(user_id):
                csrf_protect
                if request.method == 'POST':
                    form = EditRaceForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        race = Race.objects.filter(id=race_id, parent_season=season_id)[0]
                        race.updateData(data)
                        race.save()
                        string = '/plan/' + str(user_id) + '/season/' + str(season_id) + '/race/' + str(race_id) + '/'
                        return HttpResponseRedirect(string)
                else:
                    mod = Race.objects.get(id=race_id)
                    form = EditRaceForm(initial=model_to_dict(mod))
                return render(request, 'plan/race_edit.html', {'form': form, 'race_id': race_id, 'season_id': season_id, 'user_id': user_id})
            else:
                messages = ('You do not have the permission to edit this profile!',)
                return render(request, 'default_sites/message_site_logged.html', {'messages': messages})
        messages = ('To see the profile, please, log in.',)
        return render(request, 'default_sites/message_site.html', {'messages': messages})   

    def raceDelete(request, user_id, season_id):
        if request.user.is_authenticated:
            if str(request.user.id) == str(user_id):
                csrf_protect
                if request.method == 'POST':
                    raceList = []
                    if 'deleteRaces' in request.POST:
                        if Season.objects.filter(parent_user=user_id):
                            selection = request.POST.getlist('raceSelection')
                            raceList = Race.objects.filter(id__in=selection, parent_season=season_id)
                    elif 'deleteRacesAll' in request.POST:
                        raceList = Race.objects.filter(parent_season=season_id)
                    for race in raceList:
                        race.delete()
        return redirect('plan:season', user_id, season_id)

    def raceDeleteAll(request, user_id, season__id, race_id):
        pass

class PlanView(generic.View):

    def new_plan(request, user_id, season_id):
        if request.user.is_authenticated():
            if str(request.user.id) == user_id:
                csrf_protect
                if request.method == 'POST':
                    form = NewPlanForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        plan = Plan()
                        plan.save_data(data, season_id)
                        plan.save()
                        
                        with connection.cursor() as cursor:
                            cursor.execute("SELECT * FROM plan_weeklyhours WHERE annualHours = '{}'".format(plan.annualHours))
                            weeklyHours = cursor.fetchone()
                        aRaces = Race.objects.filter(parent_season=season_id, priority=3)
                        allRaces = Race.objects.filter(parent_season=season_id)
                        
                        plan.createPlan(weeklyHours, request.user.profile, aRaces, allRaces)
                        plan.save()
                        string = '/plan/' + user_id + '/season/' + season_id + '/'
                        return HttpResponseRedirect(string)
                else:
                    today = date.today()
                    form = NewPlanForm()
                return render(request, 'plan/new_plan.html', {'form': form, 'user_id':user_id, 'season_id': season_id})
            messages = ('You do not have access to this site!',)
            return render(request, 'default_sites/message_site_logged.html', {'messages': messages})
        messages = ('You are not authorised to access this site!',)
        return render(request, 'default_sites/message_site.html', {'messages': messages})
    
    def plan(request, user_id, plan_id):
        plan = get_object_or_404(Plan, pk=plan_id)
        planWeeks = PlanWeek.objects.filter(parent_plan=plan_id)
        for pw in planWeeks:
            pw.prepareData()
        x, y, captions = plan.get_graph_data(planWeeks)
        return render(request, 'plan/plan.html', {'plan': plan, 'planWeeks': planWeeks, 'season_id': plan.parent_season.id, 'x':x, 'y':y, 'captions':captions})
    
    def planDelete(request, user_id, season_id):
        if request.user.is_authenticated:
            if str(request.user.id) == str(user_id):
                csrf_protect
                if request.method == 'POST':
                    planList = []
                    if Season.objects.filter(parent_user=user_id):
                        if 'deletePlans' in request.POST:
                            selection = request.POST.getlist('planSelection')
                            planList = Plan.objects.filter(id__in=selection, parent_season=season_id)
                        elif 'deletePlansAll' in request.POST:
                            planList = Plan.objects.filter(parent_season=season_id)
                        for plan in planList:
                            plan.delete()
        return redirect('plan:season', user_id, season_id)
    



