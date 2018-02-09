from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import generic
from django.views.decorators.csrf import csrf_protect

from home.forms import LoginForm, SignupForm
from plan.tokens import account_activation_token


class HomeViews(generic.View):

    def indexPage(request):
        if request.user.is_authenticated:
            return render(request, 'home/index_logged.html')
        return render(request, 'home/index.html')

    def aboutPage(request):
        if request.user.is_authenticated:
            return render(request, 'home/about_logged.html')
        else:
            return render(request, 'home/about.html')

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
        return render(request, 'home/login.html', {'form': form})

    def sign_up(request):
        if not request.user.is_authenticated():
            if request.method == 'POST':
                form = SignupForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    user.refresh_from_db()
                    user.save()
                    current_site = get_current_site(request)
                    subject = 'Activate Your MySite Account'
                    message = render_to_string('registration/acc_activate_email.html', {
                        'user': user,
                        'domain': current_site.domain,
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
            return render(request, 'home/sign_up.html', {'form': form})
        messages = ('You are already logged in!',)
        return render(request, 'default_sites/message_site.html', {'messages': messages})

    def request_denied(request):
        return render(request, 'default_sites/unauthorised_access.html')


def logout(request):
    csrf_protect
    return logout_then_login(request, login_url='/login/')