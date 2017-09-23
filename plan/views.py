from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.loader import *
from django.views import generic
import base64
from datetime import time, tzinfo
from django.utils import timezone
from plan.model.Profile import Profile
from plan.model.Season import Season
from plan.model.Race import Race
from plan.model.Plan import Plan, PlanWeek

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from plan.forms import SignupForm, EditProfileForm, NewSeasonForm, NewRaceForm, NewPlanForm
from plan.tokens import account_activation_token
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import logout_then_login
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.forms.models import model_to_dict
from datetime import date

class IndexView(generic.View):

    def index(request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/plan/' + str(request.user.id) + '/')
        return render(request, 'plan/index.html')
    
    def about(request):
        if request.user.is_authenticated:
            return render(request, 'plan/about_logged.html')
        return render(request, 'plan/about.html')

class UserView(generic.View):
    def user(request, user_id):
        seasons = get_list_or_404(Season, fk=user_id)
        return render(request, 'plan/')

    def home(request, user_id):
        if request.user.is_authenticated:
            if str(request.user.id) == user_id:
                seasons = Season.objects.filter(parent_user = request.user.id)
                return render(request, 'plan/home.html', {'user': request.user, 'seasons': seasons})
        return render(request, 'default_sites/unauthorised_access.html')
    
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
        if request.user.is_authenticated():
            if request.method == 'POST':
                form = SignupForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    user.refresh_from_db()
                    user.save()
                    current_site = get_current_site(request)
                    subject = 'Activate Your MySite Account'
                    message = render_to_string('plan/acc_activate_email.html', {
                        'user':user, 
                        'domain':current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    mail_subject = 'Activate your blog account.'
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()
                    return render(request, 'registration/confirmation_email_sent.html')
            else:
                form = SignupForm()
            return render(request, 'plan/sign_up.html', {'form': form})
        messages = ('You are already logged in!',)
        return render(request, 'default_sites/message_site.html', {'messages': messages})

    def profile(request, user_id):
        if request.user.is_authenticated:
            userProfile = User.objects.filter(id=user_id)[0]
            owner = True
            if str(user_id) != str(request.user.id):
                owner = False
            return render(request, 'plan/profile.html', {'owner': owner, 'userProfile': userProfile})
        messages = ('To see the profile, please, log in.',)
        return render(request, 'default_sites/message_site.html', {'messages': messages})
    
    def profileEdit(request, user_id):
        if request.user.is_authenticated:
            if str(request.user.id) == str(user_id):
                csrf_protect
                if request.method == 'POST':
                    form = EditProfileForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        user = User.objects.filter(id=user_id)[0]
                        user.profile.updateData(data)
                        user.save()
                        string = '/plan/' + str(user_id) + '/profile/'
                        return HttpResponseRedirect(string)
                else:
                    mod = Profile.objects.get(user_id=user_id)
                    form = EditProfileForm(initial=model_to_dict(mod))
                return render(request, 'plan/profile_edit.html', {'form': form})
            else:
                messages = ('You do not have the permission to edit this profile!',)
                return render(request, 'default_sites/message_site_logged.html', {'messages': messages})
        messages = ('To see the profile, please, log in.',)
        return render(request, 'default_sites/message_site.html', {'messages': messages})
        
    def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return render(request, 'plan/email_confirmation.html')
        else:
            return HttpResponse('Activation link is invalid!')

class SeasonView(generic.View):

    def new_season(request, user_id):
        if request.user.is_authenticated():
            if str(request.user.id) == user_id:
                csrf_protect
                if request.method == 'POST':
                    form = NewSeasonForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        if len(Season.objects.filter(user_id_id=user_id, year=data['year'])) == 0:
                            season = Season(year=data['year'], user_id_id=user_id)
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
        season = get_object_or_404(Season, pk=season_id)
        races = Race.objects.filter(parent_season=season_id)
        for race in races:
            race.time = '{:d}:{:02d}:{:02d}'.format(race.time.hour, race.time.minute, race.time.second)
        plans = Plan.objects.filter(parent_season=season_id)
        #for plan in plans:
        #    plan.count_load(PlanWeek.objects.filter(plan_id = plan.id).values_list('weeklyHours'))
        return render(request, 'plan/season.html', {'user_id': user_id, 'season': season, 'races': races, 'plans': plans})

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
        return render(request, 'plan/plan.html', {'plan': plan})

def logout(request):
    csrf_protect
    return logout_then_login(request, login_url='/login/')
    



