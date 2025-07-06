from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login as django_login, models
from .forms import LoginForm, RegistrationForm
from django.contrib.messages import add_message, constants
from django.shortcuts import redirect



def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            username = form_data.get('username')
            password = form_data.get('password')
            remember_me = form_data.get('remember_me', False)

            user = authenticate(request, username=username, password=password)

            if user is None:
                add_message(request, constants.ERROR, 'Invalid username or password')
            else:
                django_login(request, user)
                if remember_me:
                    request.session.set_expiry(60 * 60 * 24 * 365)
                else:
                    request.session.set_expiry(0)
                return redirect('index')
            
    return render(request, 'login/login.html', {'form': LoginForm()})


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            username = form_data.get('username')
            password = form_data.get('password')
            remember_me = form_data.get('remember_me', False)

            exists = models.User.objects.filter(username=username).exists()
            if exists:
                add_message(request, constants.ERROR, 'User with username already exists')
            else:
                user = models.User.objects.create_user(
                    username=username, password=password)
                django_login(request, user)
                if remember_me:
                    request.session.set_expiry(60 * 60 * 24 * 365)
                else:
                    request.session.set_expiry(0)
                return redirect('index')

    return render(request, 'login/register.html', {'form': RegistrationForm()})


def logout(request: HttpRequest) -> HttpResponse:
    django_login(request, None)
    return redirect('login')
