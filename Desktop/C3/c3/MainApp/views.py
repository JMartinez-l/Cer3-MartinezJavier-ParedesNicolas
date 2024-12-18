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


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # Verificar si el nombre de usuario de este usuario coincide con el ingresado
        if user_with_email.username != username:
            messages.error(request, 'El correo y el nombre de usuario no coinciden.')
            
        else:
            # Autenticar con el nombre de usuario y la contraseña
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Si la autenticación es exitosa, iniciar sesión
                auth_login(request, user)
                messages.success(request, f'Bienvenido, {user.username}')
                return redirect('index')
            else:
                # Contraseña incorrecta
                messages.error(request, 'Contraseña incorrecta.')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        c_password = request.POST.get('confirm_password', '')

        if password != c_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado.')
            return render(request, 'register.html')

        user = User.objects.create_user(username = username, email = email, password = password)
        clientes_group = Group.objects.get(name='Usuario')
        user.groups.add(clientes_group)
        user.save()
        messages.success(request, 'Te has registrado exitosamente. Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'register.html')

def exit(request):
    logout(request)
    return redirect('/')
