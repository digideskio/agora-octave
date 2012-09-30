from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from registration.forms import RegistrationForm

from agora.apps.snippet.models import Snippet


def code(request):
    context = {
        'snippets': Snippet.objects.public()[:5],
        'modules': None, # temp
        'forge': None, # temp
    }

    return render(request, 'code.djhtml', context)


def login_register(request):
    form = None
    next_url = None

    if request.method == 'POST':
        action = request.POST.get('action')
        next_url = request.GET.get('next') or reverse('login')

        if action == 'login':
            username = request.POST.get('username', '')
            password = request.POST.get('password1', '')

            if username and password:
                user = authenticate(username=username, password=password)
                login(request, user)

                return redirect(next_url)
            else:
                form = {
                    'password1': {
                        'errors': 'Please enter a username and password.',
                    },
                }
        elif action == 'register':
            form = RegistrationForm(request.POST)

            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(next_url)
        else:
            # The action is not set. Malicious submission?
            pass

    context = {
        'next_url': next_url,
        'form': form,
    }

    return render(request, 'login.djhtml', context)
