import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime
import json

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

