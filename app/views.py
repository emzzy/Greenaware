from django.shortcuts import redirect, render
from django.views.decorators.csrf import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from jangfront.settings import BASE_DIR
from .user_auth import *
#from .models import User, Observer, Location
#from .forms import WeatherObservationForm

# Create your views here.
def index(request):
   # print(f"Template Directory: {request}")
    return render(request, 'index.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        return user_register(request)
    elif request.method == 'GET':
        return render(request, 'authentication/register.html')
    else:
        return render(request, 'authentication/register.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':

        return user_login(request, 'authentication/login.html')
    elif request.method == 'GET':
        return render(request, 'authentication/login.html')
    return redirect('dashboard')

@login_required
@csrf_exempt
def dashboard(request):
    if request.user.user_role == 'observer':
        return render(request, 'authentication/dashboard.html')
    else:
        return render(request, 'authentication/dashboard/html')
