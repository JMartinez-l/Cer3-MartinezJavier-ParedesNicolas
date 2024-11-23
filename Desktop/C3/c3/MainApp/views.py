import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime
import json
from .forms import Formulario, CustomUserCreationForm
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


def Login(request):
    if request.method == "POST":
        form = Formulario(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            print(f"Attempting login with email: {email} and password: {password}")
            
            # Check if email and password are not None
            if email and password:
                print("Calling authenticate()")
                try:
                    user = authenticate(request, username=email, password=password)
                except Exception as e:
                    print(f"Exception during authentication: {e}")
                    form.add_error(None, "An error occurred during login")
                    return render(request, 'login.html', {'form': form})
                print(f"Authenticate returned: {user}")
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    print("Authentication failed: Invalid email or password")
                    form.add_error(None, "Invalid email or password")
            else:
                print("Form data is missing email or password")
                form.add_error(None, "Please enter both email and password")
    else:
        form = Formulario()
    
    return render(request, 'login.html', {
        'form': form
    })


def exit(request):
    logout(request)
    return redirect('/')
