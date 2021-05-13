from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .forms import RegisterForm, EventForm
from .services.event import EventService
from .services.security import SecurityService
from .services.telegram import TelegramService


@csrf_exempt
def webhook(request):
    service = TelegramService()
    service.manage_request(request.body)
    return HttpResponse()


@login_required(login_url='login')
def index(request):
    return render(request=request, template_name="index.html")


def test(request):
    return JsonResponse({'status': 'true', 'message': 'worked'})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


@login_required(login_url='login')
def security_code(request):
    security_service = SecurityService()
    code = security_service.get_or_create_security_code(request.user.id)
    context = {'security_code': code.code}
    return render(request=request, template_name="security_code.html", context=context)


@login_required(login_url='login')
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event_service = EventService()
            event_service.insert(request, form.cleaned_data)
            return HttpResponseRedirect('/')
    else:
        form = EventForm()
    return render(request=request, template_name='create_event.html', context={'form': form})
