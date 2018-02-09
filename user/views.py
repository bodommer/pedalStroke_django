from django.contrib.auth import login
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import generic
from django.views.decorators.csrf import csrf_protect

from user.model.Profile import Profile
from plan.tokens import account_activation_token
from user.forms import EditProfileForm


class ProfileView(generic.View):

    def profile(request, user_id):
        if request.user.is_authenticated:
            userProfile = User.objects.filter(id=user_id)[0]
            owner = True
            if str(user_id) != str(request.user.id):
                owner = False
            return render(request, 'user/profile.html', {'owner': owner, 'userProfile': userProfile})
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

