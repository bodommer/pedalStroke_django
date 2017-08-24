from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views import generic
from plan.model.User import User
from plan.model.Season import Season
from plan.model.Race import Race
from plan.model.Plan import Plan

from .forms import LoginForm
from django.views.decorators.csrf import csrf_protect

class IndexView(generic.ListView):
    template_name = 'plan/index.html'
    context_object_name = 'user_list'
    
    def get_queryset(self):
        users = User.objects.order_by('-age')
        for user in users:
            user.seasons = get_list_or_404(Season, user_id = user.id)
        return users
    
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

def user(request, user_id):
    seasons = get_list_or_404(Season, fk=user_id)
    return render(request, 'plan/')

def home(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    seasons = get_list_or_404(Season, user_id=user_id)
    return render(request, 'plan/user.html', {'user': user, 'seasons': seasons})

def new_season(request):
    return HttpResponse("You're creating a new season")

def new_race(request):
    return HttpResponse("You're creating a new season.")

def season(request, user_id, season_id):
    season = get_object_or_404(Season, pk=season_id)
    races = get_list_or_404(Race, season_id=season_id)
    plans = get_list_or_404(Plan, season_id=season_id)
    return render(request, 'plan/season.html', {'season': season, 'races': races, 'plans': plans})

def new_plan(request):
    return HttpResponse("You're looking at question %s." % user_id)

def plan(request, user_id, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    return render(request, 'plan/plan.html', {'plan': plan})

def login(request):
    csrf_protect
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user_list = User.objects.order_by('-age')
            print(form.fields['username'])
            user_id = get_object_or_404(User, name=data['username']).id
            string = '/plan/' + str(user_id) + '/'
            return HttpResponseRedirect(string)
    else:
        form = LoginForm()
    return render(request, 'plan/login.html', {'form': form})

def sign_up(request):
    return render(request, 'plan/sign_up.html')

def about(request):
    return render(request, 'plan/about.html')
