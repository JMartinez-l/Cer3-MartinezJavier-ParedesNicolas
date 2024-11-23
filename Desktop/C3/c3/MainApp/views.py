import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime
import json
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def index(request):
    # Get current year
    year = datetime.now().year
    
    # Make API request to get holidays
    api_url = f'https://calendarific.com/api/v2/holidays'
    params = {
        'api_key': settings.API_KEY,
        'country': 'CL',
        'year': year
    }
    
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        print("API Response:", data)  # Debugging
        holidays = data['response']['holidays']
        holiday_dates = {
            holiday['date']['iso']: holiday['name'] 
            for holiday in holidays
        }
    except Exception as e:
        print("Error fetching holidays:", str(e))
        holiday_dates = {}
    
    return render(request, 'index.html', {'holidays': json.dumps(holiday_dates)})

def Register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('/')
        else:
            data['form'] = user_creation_form

    return render(request, 'register.html', data)



def exit(request):
    logout(request)
    return redirect('/')
